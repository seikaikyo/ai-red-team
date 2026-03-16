---
title: 修復 stats API 回應過慢 (2s -> 目標 <500ms)
type: fix
status: in-progress
created: 2026-03-16
---

# 修復 stats API 回應過慢

## 變更內容
1. database.py - 加入 SQLAlchemy 連線池設定，複用 Neon 連線
2. stats.py - 合併 6 個 SQL 查詢為 1-2 個，減少往返

## 影響範圍
- `backend/database.py`
- `backend/routers/stats.py`

## 測試計畫
1. curl 測試 /api/stats 回應時間 < 500ms
2. 確認回傳資料結構不變
