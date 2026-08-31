---
title: 安全強化 - Security Audit 修復
type: fix
status: done
created: 2026-03-16
closed: 2026-08-31
---

# 安全強化 - Security Audit 修復

## 變更內容
依優先級修復 security-audit 發現的 16 個問題 (2 CRITICAL + 4 HIGH + 6 MEDIUM + 4 LOW)

## 影響範圍
- `backend/auth.py` - C-1 認證繞過修復
- `backend/config.py` - L-1 啟動驗證
- `backend/main.py` - H-4 rate limit, M-6 CORS, L-2/L-4
- `backend/middleware.py` - M-1 CSP, M-2 XSS header
- `backend/models.py` - H-2 長度限制, M-3 model 白名單, M-4 UUID 驗證
- `backend/routers/stats.py` - M-5 SQL 模式, H-3 認證
- `backend/routers/tests.py` - H-3 認證
- `backend/routers/templates.py` - H-3 認證
- `backend/services/runner.py` - H-1 SSRF
- `frontend/src/composables/useApiKey.ts` - C-2 儲存方式
- `frontend/vercel.json` - M-1 CSP header

## 測試計畫
1. curl 測試所有 API 端點認證
2. 前端建構通過
3. E2E 煙霧測試

## 結案（2026-08-31）

C-1 與 H-1 當時只做了部分收窄，2026-08-31 的複查發現三個殘留問題並已修完：
認證旁路改為顯式開關（原本以資料庫種類推測環境）、SSRF 過濾器補上
IPv4-mapped IPv6 與 CGNAT 兩個繞過口並關閉轉址跟隨、伺服器 LLM 金鑰不再
跟隨呼叫端指定的網址。回歸測試見 `backend/tests/test_security_controls.py`。
詳見 `openspec/changes/fix-security-audit-remediation.md`。
