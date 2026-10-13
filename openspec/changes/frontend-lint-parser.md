# 補宣告 vue-eslint-parser，前端 lint 恢復可跑

- **type**: build
- **建立日期**: 2026-10-14
- **狀態**: 完成

## 背景

2026-10-13 沙盒第 3 批驗收，`frontend/` 跑 `npm run lint` 直接失敗：eslint-plugin-vue 10 把 vue-eslint-parser 列為必要的 peer dependency，package.json 沒宣告。使用者決定修。

## 變更內容

- devDependencies 加 `vue-eslint-parser ^10.4.1`。
- 補上之後 lint 能跑，剩 1 個錯誤：`src/App.vue:54` 的 `document` 被 `no-undef` 判成未定義。所有元件的 `<script>` 都是 `lang="ts"`，未定義名稱由 vue-tsc 檢查；typescript-eslint 的設定對 .ts 檔就是關掉 `no-undef`（node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslint-recommended-raw.js），`eslint.config.js` 的 .vue 區塊照做。

## 影響範圍

只動 lint 設定與開發相依，建置產物不變。

## UI 規格

無。

## 測試計畫

- `npm run lint`：0 錯誤（376 個既有警告，多數是 vue/max-attributes-per-line，不在本次範圍）。
- `npm run build`（vue-tsc -b 加 vite build）通過。
- `vite preview` 首頁在 375 寬正常渲染、無頁面錯誤。
- `npm audit` 加套件前後都是 3 筆 high，沒有新增。
