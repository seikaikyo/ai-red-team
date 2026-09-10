# 修補 Dependabot 未修警示（10 筆）

- **type**: fix
- **建立日期**: 2026-09-10

## 背景

2026-09-10 起 seikaikyo/security-watch 的採集器（`.github/workflows/github-alerts.yml`）每日抓取 19 個 repo 的 Dependabot 警示。這是該機制上線後第一次量到本 repo 的未修數字，在此之前每日資安巡檢的 GitHub 段都記為「無法檢查」，等於這些警示長期無人監看。

本 repo 有 10 筆未修警示，high 5 筆、medium 3 筆、low 2 筆，全部落在 `frontend/package-lock.json`。10 筆來自 6 個套件。

## 變更內容

| 套件 | 筆數 | 目標版本 |
| --- | --- | --- |
| vite | 5 | 7.3.5 |
| brace-expansion | 1 | 5.0.7 |
| flatted | 1 | 3.4.2 |
| @humanfs/node | 1 | 0.16.8 |
| esbuild | 1 | 0.28.1 |
| postcss-selector-parser | 1 | 7.1.3 |

全部為同一主版本內的修補。做法是在 `frontend/` 下 `npm audit fix` 只更新 lockfile。

## 影響範圍

| 對象 | 影響 |
| --- | --- |
| 執行期行為 | 無。全部是建構期與檢查工具鏈（vite、esbuild、flatted、@humanfs/node、postcss-selector-parser、brace-expansion），不進入瀏覽器執行的產物。 |
| package.json 或 go.mod 的直接相依宣告 | 不改動，只更新 `frontend/package-lock.json`。 |
| 部署 | Vercel 依 git push 自動部署。 |

## UI 規格

無 UI 變更。

## 測試計畫

1. `npm run build`（vue-tsc -b 加 vite build）通過。
2. 建構通過才推送。
3. 推送後重新觸發 security-watch 的 github alerts workflow，確認本 repo 的 `open_total` 歸零或僅剩無修復版本者。
