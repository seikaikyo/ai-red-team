---
title: 企業產品等級強化
type: refactor
status: completed
created: 2026-03-16
---

# 企業產品等級強化

## 變更內容

根據完整系統審查，依優先級修復以下問題：

### P0 - 資安 (上線阻斷項)
1. SSRF 修復 - base_url allowlist 驗證
2. Rate Limiting - slowapi 限流
3. API Key 認證 - Bearer token 保護寫入/執行端點
4. CORS 限縮 - 正式環境白名單
5. 安全 headers - CSP, HSTS, X-Frame-Options, X-Content-Type-Options

### P1 - 可靠度
6. 輸入驗證 - category/severity 用 Enum
7. Pydantic deprecated 修復 - ConfigDict
8. 全域 exception handler
9. 結構化日誌
10. 分頁加入 total count

### P1 - UI/UX
11. HTML title 修正 + 動態 page title
12. 響應式設計 - mobile/tablet/desktop
13. 無障礙基礎 - ARIA labels, 色彩對比
14. 404 頁面
15. 抽離 inline CSS

### P2 - SEO
16. Meta tags (description, og:*)
17. Canonical URL + Open Graph

### P2 - 維運
18. 停用 keep-alive workflow (改用 UptimeRobot)

## 影響範圍

### 後端 (新建 2 檔 + 修改 6 檔)
- `backend/auth.py` (新建) - API Key 認證 + SSRF 防護
- `backend/middleware.py` (新建) - 安全 headers
- `backend/main.py` - 安全 middleware, exception handler, rate limit, 結構化日誌
- `backend/config.py` - ConfigDict, 新增 app_api_key/rate_limit 設定
- `backend/models.py` - Enum 驗證, field_validator
- `backend/routers/templates.py` - 認證 + total count
- `backend/routers/tests.py` - 認證 + SSRF 防護 + 限流
- `backend/requirements.txt` - slowapi

### 前端 (新建 1 檔 + 修改 11 檔)
- `frontend/src/views/NotFoundView.vue` (新建) - 404 頁面
- `frontend/index.html` - title, meta description, OG tags, canonical
- `frontend/src/App.vue` - 響應式 mobile menu, ARIA labels, lang 動態切換
- `frontend/src/style.css` - 完整 CSS 重構 (CSS 變數、響應式、utility classes)
- `frontend/src/router/index.ts` - 404 route, afterEach page title
- `frontend/src/views/DashboardView.vue` - CSS class 取代 inline
- `frontend/src/views/RunnerView.vue` - CSS class + form labels
- `frontend/src/views/TemplatesView.vue` - CSS class + ARIA
- `frontend/src/views/ResultsView.vue` - CSS class + ARIA
- `frontend/src/views/ReportView.vue` - CSS class
- `frontend/src/config/i18n/en.ts` - 新增 common.* keys
- `frontend/src/config/i18n/zh.ts` - 新增 common.* keys
- `frontend/src/config/i18n/ja.ts` - 新增 common.* keys

### CI/CD
- `.github/workflows/keep-alive.yml` - 移除 schedule，改用 UptimeRobot

## 測試結果
1. 後端 17 個既有測試全部通過
2. 前端 vue-tsc --noEmit 通過
3. 前端 vite build 通過 (914ms)

## Checklist
- [x] P0 資安修復
- [x] P1 可靠度修復
- [x] P1 UI/UX 修復
- [x] P2 SEO 修復
- [x] P2 維運修復
- [x] 全部測試通過
