---
title: 中英日三語系支援
type: feature
status: in-progress
created: 2026-02-27
---

# 中英日三語系支援

## 變更內容

1. **UI 介面三語切換** - Sidebar、按鈕、表頭、表單標籤、placeholder 支援 zh-TW / en / ja
2. **Seed Data 三語版本** - 32 個攻擊模板擴充為中/英/日三語版本，方便交叉測試 LLM 多語安全性

## 影響範圍

- `frontend/src/composables/useI18n.ts` (新增)
- `frontend/src/config/i18n/` (新增，三語翻譯檔)
- `frontend/src/App.vue` (語言切換器)
- `frontend/src/views/*.vue` (所有 5 個頁面文字替換為 i18n key)
- `frontend/src/config/categories.ts` (分類標籤多語)
- `backend/seed/templates.json` (擴充三語模板)

## 測試計畫

1. 切換語言後所有頁面文字正確顯示
2. 三語 seed data 正確載入
3. 跨語言測試流程正常運作
