---
title: 功能性缺口修復 - API Key UI、Neon PostgreSQL、README
type: fix
status: in-progress
created: 2026-03-16
---

# 功能性缺口修復

## 變更內容

### 1. 前端 API Key 輸入機制
- Settings 面板：localStorage 存 apiKey
- 所有寫入/執行 fetch 自動帶 X-API-Key header
- 參考 jlpt-n1-learner 的做法

### 2. 資料庫遷移至 Neon PostgreSQL
- config.py DATABASE_URL 改為 Neon 連線字串
- requirements.txt 加入 psycopg[binary]
- Render 環境變數設定 DATABASE_URL
- seed data 邏輯不變（空表時自動載入）

### 3. README port 修正 + Favicon
- README.md 5174 → 5175
- 替換 Vite 預設 favicon

## 影響範圍
- `frontend/src/composables/useTemplates.ts` - 加 header
- `frontend/src/composables/useTestRunner.ts` - 加 header
- `frontend/src/composables/useApiKey.ts` (新建) - API Key 管理
- `frontend/src/App.vue` - Settings 按鈕
- `backend/config.py` - DATABASE_URL 預設值
- `backend/requirements.txt` - psycopg
- `README.md` - port 修正
- `frontend/public/favicon.svg` (新建)
- `frontend/index.html` - favicon 路徑

## 測試計畫
1. 無 API Key 時 GET 端點正常，寫入端點 401
2. 有 API Key 時所有操作正常
3. Neon 連線測試
4. 後端 pytest 通過
5. 前端 vue-tsc + vite build 通過
