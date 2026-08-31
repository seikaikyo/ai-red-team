# 資安稽核修復：金鑰外送、SSRF 繞過、認證旁路

- **Type**: fix
- **Status**: done
- **Created**: 2026-08-31

## 背景

2026-08-31 對本 repo 做防禦性資安稽核，三項發現皆已由讀碼與實測確認。三項都落在本專案自己宣稱在防的攻擊面上，且 `openspec/changes/security-hardening.md` 曾宣稱修復 C-1 與 H-1，實際只做了部分收窄。

## 變更內容

### 1. 伺服器金鑰不再跟隨呼叫端指定的網址（High）

`backend/services/runner.py` 原本把請求帶來的 `base_url` 與伺服器自己的 `OPENAI_API_KEY` 湊成同一個 client，等於後端主動把金鑰放進 `Authorization` 標頭送到請求者指定的主機。

改為：`base_url` 由呼叫端指定時一律不附掛伺服器憑證（送 `no-key`），只有使用伺服器自己設定的 `custom_llm_base_url` 時才使用伺服器憑證。自架 LLM（Ollama / vLLM / LM Studio）本來就不驗金鑰，功能不受影響。

### 2. SSRF 過濾器補三個繞過口（High）

`backend/auth.py`：

- IPv4-mapped IPv6（`::ffff:127.0.0.1`）在 Python 的 `ipaddress` 中與 IPv4 網段比對恆為 False，原本可直接繞過。新增 `_normalize_ip` 先還原成 IPv4 再比對。
- 補上 `100.64.0.0/10`（CGNAT）並改用 `is_global` 當主判準，涵蓋保留與特殊用途網段。
- openai SDK 預設 `follow_redirects=True`，通過驗證的公網主機回 302 即可導向內網。改為建立 client 時明確帶入 `follow_redirects=False` 的 httpx client。

### 3. 認證旁路改為顯式開關（Medium）

`backend/auth.py` 原本以「資料庫是不是 SQLite」推測執行環境來決定是否跳過驗證，而 `config.py` 的 `database_url` 預設值就是 SQLite。金鑰被清空時服務照常啟動、不報錯、不記 log，寫入與執行端點全開。

改為新增 `allow_insecure_auth` 設定（預設 False），只有顯式設為 true 才跳過驗證；`app_api_key` 為空且未開該旗標時一律 fail closed 回 503。`backend/main.py` 的啟動警告移出 `not sqlite` 分支，任何組態缺金鑰都會在啟動時記錄。

### 4. 自架 LLM 的 localhost 目標改為顯式開關

`validate_base_url` 擋掉 localhost，與 README 宣傳的自架 LLM 用途及 UI 的 localhost 預設值衝突，該功能實際一按就錯。新增 `allow_private_base_url` 設定（預設 False），本機開發顯式開啟後才允許私網與 loopback 目標，正式部署維持封鎖。

### 5. 授權條款宣告一致化

`LICENSE` 為專有授權，但 `README.md` 掛 MIT 徽章並在 License 段寫 MIT。README 兩處改為與 LICENSE 一致。

## 影響範圍

- `backend/auth.py`、`backend/services/runner.py`、`backend/config.py`、`backend/main.py`、`README.md`
- 不改資料模型、不改 API 介面形狀、不動 seed 樣板庫
- 行為變更：未設 `APP_API_KEY` 的部署由「靜默全開」改為「回 503」。這是刻意的 fail closed，部署前必須設定該環境變數。

## UI 規格

無前端變更。

## 測試計畫

新增 `backend/tests/test_security_controls.py`：

1. IPv4-mapped IPv6 的 loopback 與 metadata 位址被擋。
2. CGNAT 網段被擋。
3. 公網位址放行。
4. 非 http/https scheme 被擋。
5. 呼叫端指定 `base_url` 時不附掛伺服器金鑰。
6. 未指定 `base_url` 時使用伺服器設定與憑證。
7. `app_api_key` 為空且未開旗標時回 503，不放行。
8. 開啟 `allow_insecure_auth` 時才回 dev。
9. 錯誤或缺少 API key 時回 401。
