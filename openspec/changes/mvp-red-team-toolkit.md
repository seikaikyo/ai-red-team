---
title: AI Red Teaming Toolkit MVP
type: feature
status: in-progress
created: 2026-02-27
---

# AI Red Teaming Toolkit MVP

## 背景

為準備 Mercor AI Red-Teamer 職位，建立一個系統化的 LLM 對抗測試工具。同時作為 portfolio 展示 AI safety 實務能力。

## 技術選型

| 層級 | 技術 | 理由 |
|------|------|------|
| Frontend | Vite + Vue 3 + TypeScript + PrimeVue 4 | 統一技術棧 |
| Backend | FastAPI + SQLModel | 統一技術棧 |
| Database | Neon PostgreSQL | 統一雲端服務 |
| AI | Anthropic API (Claude) | 已有 API Key，主要測試對象 |
| Port | 前端 5174 / 後端 8005 | 接在現有 pm2 配置後面 |

## MVP 功能範圍

### 1. 攻擊模板管理

- 模板 CRUD（建立、編輯、刪除）
- 分類體系：prompt_injection / jailbreak / bias / safety_bypass / multilingual
- 嚴重等級標記：low / medium / high / critical
- 模板支援變數替換 `{{variable}}`，執行時填入

**資料結構：**
```
AttackTemplate:
  id: UUID
  name: str                    # 模板名稱
  category: str                # 攻擊類別
  severity: str                # 嚴重等級
  description: str             # 說明（中文）
  prompt_template: str         # 攻擊 prompt，支援 {{var}}
  variables: list[str]         # 變數名稱列表
  expected_behavior: str       # 預期安全行為（用於判斷成功/失敗）
  tags: list[str]              # 標籤
  language: str                # en / zh / mixed
  created_at: datetime
  updated_at: datetime
```

### 2. 測試執行

- 單次執行：選模板 → 填變數 → 送出 → 看回應
- 批次執行：選多個模板 → 一次跑完 → 彙整結果
- 目標模型設定：model name + max_tokens + temperature
- 執行時記錄完整 request/response

**資料結構：**
```
TestRun:
  id: UUID
  template_id: UUID
  model: str                   # claude-sonnet-4-20250514 等
  prompt_sent: str             # 實際送出的 prompt（變數已替換）
  response: str                # 模型回應
  success: bool | None         # 攻擊是否成功（手動或自動判定）
  notes: str                   # 測試者備註
  duration_ms: int             # 回應時間
  created_at: datetime
```

### 3. 結果 Dashboard

- 總測試數 / 成功率 / 各類別分布
- 依類別篩選、依時間排序
- 單一測試結果詳情（prompt + response 對照）

### 4. 報告匯出

- Markdown 格式匯出
- 包含：測試摘要、攻擊向量、成功案例、建議修復方向
- 檔名：`report-{model}-{date}.md`

### 5. 內建模板庫（Seed Data）

預建 30+ 個攻擊模板，涵蓋五大類別：

| 類別 | 數量 | 範例 |
|------|------|------|
| prompt_injection | 8 | 指令覆蓋、system prompt 洩露、delimiter 注入 |
| jailbreak | 8 | DAN 類、角色扮演、編碼繞過、多輪遞進 |
| bias | 6 | 性別偏見、種族偏見、國籍偏見（同一問題換變數） |
| safety_bypass | 5 | 有害指引、敏感資訊生成、CSAM 邊界測試 |
| multilingual | 5 | 中英混合攻擊、語言切換繞過、翻譯指令注入 |

## 影響範圍

全新專案，不影響既有系統。

```
ai-red-team/
  frontend/
    src/
      views/
        Dashboard.vue          # 總覽頁面
        Templates.vue          # 模板管理
        TestRunner.vue         # 測試執行
        Results.vue            # 結果列表
        ReportExport.vue       # 報告匯出
      composables/
        useTemplates.ts        # 模板 CRUD
        useTestRunner.ts       # 測試執行邏輯
        useStats.ts            # 統計數據
      components/
        TemplateCard.vue       # 模板卡片
        TestResultRow.vue      # 結果列表行
        StatsPanel.vue         # 統計面板
        PromptEditor.vue       # Prompt 編輯器（支援變數高亮）
      router/
        index.ts
      config/
        api.ts
        categories.ts          # 攻擊類別定義
      utils/
        report-export.ts       # 報告產生器
    package.json
    vite.config.ts

  backend/
    main.py                    # FastAPI app
    config.py                  # Settings
    models.py                  # SQLModel 定義
    routers/
      templates.py             # 模板 CRUD API
      tests.py                 # 測試執行 API
      stats.py                 # 統計 API
    services/
      runner.py                # 模型測試執行引擎
      scorer.py                # 自動評分（關鍵字比對）
    seed/
      templates.json           # 預建模板資料
    requirements.txt
```

## UI/UX 規格

- **配色**: PrimeVue Aura 主題，安全相關用紅色系強調
- **間距**: 4px 基數 (8/12/16/24/32px)
- **佈局**: 左側 sidebar 導航 + 右側內容區
- **響應式**: desktop-first（這是工作工具，不是手機 app）
- **表格**: PrimeVue DataTable，支援排序、篩選、分頁

## 測試計畫

1. 模板 CRUD：建立 → 編輯 → 刪除 → 確認列表更新
2. 單次測試：選模板 → 填變數 → 執行 → 確認有回應 + 記錄
3. 批次測試：選 3 個模板 → 批次執行 → 確認 3 筆結果
4. Dashboard：確認統計數字正確
5. 報告匯出：下載 .md → 確認格式完整
6. Seed Data：啟動後確認 30+ 模板存在

## 實作順序

| 階段 | 內容 | 預估檔案數 |
|:----:|------|:----------:|
| 1 | 後端骨架 + DB schema + 模板 CRUD API | 6 |
| 2 | 前端骨架 + 路由 + 模板管理頁面 | 8 |
| 3 | 測試執行引擎 + 執行頁面 | 4 |
| 4 | Dashboard 統計 + 結果列表 | 4 |
| 5 | 報告匯出 + Seed Data | 3 |
| 6 | 整合測試 + 修正 | 0 |

## Checklist

- [ ] 後端 FastAPI 骨架 + CORS
- [ ] SQLModel schema (AttackTemplate + TestRun)
- [ ] Neon DB 建表
- [ ] 模板 CRUD API
- [ ] 測試執行 API
- [ ] 統計 API
- [ ] 前端 Vite + Vue 3 + PrimeVue 初始化
- [ ] 路由設定 (5 頁面)
- [ ] 模板管理頁面 (列表 + 新增/編輯 Drawer)
- [ ] 測試執行頁面 (模板選擇 + 變數填入 + 回應顯示)
- [ ] 結果列表頁面
- [ ] Dashboard 統計面板
- [ ] 報告 Markdown 匯出
- [ ] Seed Data 30+ 攻擊模板
- [ ] pm2 ecosystem 配置
