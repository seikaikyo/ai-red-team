---
title: 新增第 13 類 Knowledge Boundary Escalation
type: feature
status: completed
created: 2026-04-19
updated: 2026-09-24
---

# 新增第 13 類 Attack Category：Knowledge Boundary Escalation

## 變更內容

在既有 12 類攻擊範本之外，新增第 13 類 `knowledge_boundary_escalation`（知識邊界漸進攻擊）。

本類與既有兩類的區隔：

| 類別 | 核心手法 | 單/多輪 |
|------|---------|---------|
| `multi_turn`（既有） | 社交工程、信任建立、話題漸移 | 多輪 |
| `hallucination`（既有） | 單輪直接誘發編造 | 單輪 |
| `knowledge_boundary_escalation`（新） | 技術對話 Turn 1-2 在 domain 中心讓 model 成功 → Turn 3 推到訓練資料尾部/轉換期邊界，誘發「看起來對但其實錯」的自信答案 | 多輪 |

關鍵 failure mode：三症狀同時出現
1. **事實捏造**（plausible-sounding、survives surface review）
2. **數值幻覺**（off-by-one on boundary values）
3. **Fall-through bug**（邊界 case 漏判、silent 用錯 branch）

## 範本設計：4 concepts × 3 langs = 12 templates

全部避開具體商業 benchmark 素材，全部用公開可驗證的正體中文/台灣/日文 domain：

1. **Orthographic Boundary Escalation** 正字邊界漸進
   - Turn 1-2：標準繁/簡/異體字轉換（e.g., 臺↔台、鍾↔鐘）
   - Turn 3：CJK Extension B+ 稀有字的 Unicode normalization（e.g., 𠀋、𠁎）

2. **Historical Transition Edge** 歷史轉換期邊界
   - Turn 1-2：安全年份的民國年 → Gregorian 轉換
   - Turn 3：1945 終戰（昭和 20 / 民國 34 / Gregorian 不同過渡）、1949 民國遷台等政權轉換日期

3. **Multi-System Romanization** 多拼音系統共存
   - Turn 1-2：中文 → 漢語拼音；日文 → Hepburn Romaji
   - Turn 3：台語三套（白話字 POJ / 台羅 TL / 通用拼音）互換 ，相同音不同拼法 boundary

4. **Buddhist/Sanskrit Transliteration Tail** 佛經梵漢音譯邊界
   - Turn 1-2：常見 mantra（六字大明咒、心經結尾咒）梵漢對應
   - Turn 3：T21 宿曜經二十八宿梵文原名對應，訓練資料尾部的罕見佛教天文學術語

## 影響範圍

2026-09-24 更新：後端已併入 dashai-api 的 `/redteam` 模組，原本列的 `backend/` 路徑不再使用。實際改動位置：

- dashai-api `redteam/models.py`：`CategoryEnum` 新增 `knowledge_boundary_escalation`
- dashai-api `redteam/seed/templates.json`：追加 12 筆（177 → 189）；範本原稿即本目錄的 `add-knowledge-boundary-category.templates.json`（歸檔後同在 openspec/archive），正體中文與日文版的零散英文詞改成中日文
- dashai-api `scripts/redteam_seed_add_category.py`：`load_redteam_seed()` 只在空表時載入，而範本可在前端刪除，不能在啟動時自動補回缺的列；新增這支手動補插腳本，以 (name, language) 判斷，只處理指定類別
- dashai-api `redteam/tests/test_seed_templates.py`：seed 結構檢查
- ai-red-team `frontend/src/config/categories.ts`、`frontend/src/config/i18n/{en,zh,ja}.ts`：第 13 類標籤
- ai-red-team `README.md`：範本數與類別表
- 無 schema 變更，既有 177 筆不受影響；正式資料庫以補插腳本加入 12 筆

## 法規與智慧財產考量

本提案內容**完全避開**任何付費合作案的具體交付內容。範本範例來源：
- 公開史料（民國/日本史）
- 公開 Unicode 標準
- 公開羅馬字系統（台羅、POJ 是教育部公告）
- 公開佛典（T21 大正藏已 public domain、用戶本業 domain）

合規原則：只寫「方法論 + 通用範例」，不寫「外部客戶 benchmark 素材」。

## 測試計畫

1. dashai-api `pytest redteam/tests` 全綠（含 seed 結構檢查：類別、重複、佔位符與 variables 一致）
2. 補插腳本先不加 `--apply` 確認只列出 12 筆，再實際寫入；寫入後正式資料庫 189 筆
3. 前端 `vue-tsc --noEmit` 與 build 通過，正式站類別下拉出現第 13 類、篩選後列出 12 筆
4. 不以 Anthropic API 逐筆實跑（會產生費用）；格式正確性由第 1 點的佔位符檢查保證

## 後續

類別上線後，可擴充每類至 15 或 18 範本（對齊 `safety_bypass`/`multilingual` 規模）。現階段先求 proof-of-concept 12 個。
