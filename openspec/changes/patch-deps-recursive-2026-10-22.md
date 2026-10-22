# 修補前端相依漏洞

- **type**: fix
- **建立日期**: 2026-10-22

## 背景

2026-10-22 每日資安巡檢的 osv-scanner 改成遞迴掃描後，才掃到子目錄的鎖定檔。本 repo 有兩處：

1. frontend/package-lock.json：3 個套件有同主版號的修補版（osv 列 7 筆）。修補前 `npm audit --omit=dev`：high 3（含開發相依共 high 4）。
2. backend/requirements.txt：只釘了頂層套件，間接相依（anyio、certifi、idna、pygments、tqdm）沒有釘版，osv 列 16 筆。這部分本提案不處理，見剩餘風險。

## 變更內容

前端（範圍內 `npm update`，不改 package.json）：

- vue 3.5.29 → 3.5.44（連帶 @vue/server-renderer、@vue/compiler-*、@vue/runtime-*、@vue/reactivity、@vue/shared 同步到 3.5.44，@babel/parser 與 @babel/types 隨 compiler-sfc 升到 7.29.x）
- vite 7.3.6 → 7.3.7（連帶 postcss 8.5.28 → 8.5.31、nanoid 3.3.18 → 3.3.20）
- source-map-js 1.2.1 → 1.2.2

不升主版號、不加 overrides、不跑 `npm audit fix`、不改程式碼，只動 lock 檔。

## 影響範圍

| 對象 | 影響 |
| --- | --- |
| 執行期行為 | 無功能變更，只升修補版。 |
| 依賴檔 | frontend/package-lock.json。 |
| 部署 | Vercel 依 git push 自動部署。 |

## 剩餘風險

1. 前端修補後 `npm audit`：0 筆。
2. 後端鎖定（requirements.in 加 uv pip compile 產出附雜湊值的 requirements.txt）暫緩：CI 的 backend job 用 Python 3.11，Render 用 3.12.12。以 `--python-version 3.12` 編出的鎖定檔會釘 deprecated 3.0.0（經 slowapi → limits 引入），這版要求 Python 3.12 以上，CI 在 3.11 安裝會失敗。改用 `--python-version 3.11` 編譯時，3.12 的解析結果完全相同，只多出 3.11 專用的 deprecated 1.3.1。採用哪一種（或把 CI 升到 3.12）待決定後另開提交。

## UI 規格

無 UI 變更。

## 測試計畫

1. 前端 `npm ci` 後 `npx vue-tsc --noEmit`、`npm run build`、`npm run lint`，修補前後比對：vue-tsc 與 build 前後都成功，lint 前後都是 0 error、376 warning。
2. 推送後確認 CI 與 Vercel 部署成功，並重跑每日巡檢確認 osv-details 的前端漏洞數歸零。
