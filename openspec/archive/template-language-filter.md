---
title: 模板庫語言連動篩選
type: feature
status: completed
created: 2026-02-27
---

# 模板庫語言連動篩選

## 變更內容
模板庫預設跟隨 UI 介面語言篩選，同時保留手動語言下拉讓使用者切換。

## 影響範圍
- `backend/routers/templates.py` — API 新增 `language` 查詢參數
- `frontend/src/composables/useTemplates.ts` — `fetchTemplates` 傳入 language 參數
- `frontend/src/views/TemplatesView.vue` — 預設帶入 locale，加語言篩選下拉
- `frontend/src/views/RunnerView.vue` — filteredTemplates 加入語言篩選邏輯

## 測試計畫
1. 切換 UI 語言到中文，模板庫和 Runner 預設只顯示 zh 模板
2. 手動切換語言下拉到 en，確認顯示英文模板
3. 切換到「全部」，確認顯示所有語言模板
4. 確認新建模板時 language 預設跟隨 UI 語言

## Checklist
- [ ] 後端 API 支援 language 篩選
- [ ] TemplatesView 預設連動 locale
- [ ] RunnerView 預設連動 locale
- [ ] 新建模板預設語言跟隨 locale
