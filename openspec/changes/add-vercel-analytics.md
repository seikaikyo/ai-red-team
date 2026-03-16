---
title: 加入 Vercel Analytics
type: feature
status: in-progress
created: 2026-03-16
---

# 加入 Vercel Analytics

## 變更內容
安裝 `@vercel/analytics` 並在 main.ts 注入，追蹤網站流量。

## 影響範圍
- `frontend/package.json` - 新增依賴
- `frontend/src/main.ts` - import 並 inject analytics

## 測試計畫
1. vue-tsc 型別檢查通過
2. vite build 建構通過
