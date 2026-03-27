# AI Red Team - Design System

> 從現有程式碼萃取，所有 UI 開發必須遵循本規範。

## 色彩

### 主要色彩

| Token | 值 | 用途 |
|-------|-----|------|
| `--color-danger` | #e74c3c | 錯誤、Attack Success |
| `--color-warning` | #f39c12 | 警告、中性狀態 |
| `--color-success` | #27ae60 | 成功、Blocked 狀態 |
| `--color-info` | #2980b9 | 資訊標籤 |
| `--color-text` | #1e293b | 主要文字 (Slate 800) |
| `--color-text-secondary` | #64748b | 次要文字 (Slate 500) |
| `--color-text-muted` | #64748b | 淡化文字 |
| `--color-bg` | #f8f9fa | 頁面背景 |
| `--color-card` | #fff | 卡片背景 |
| `--color-border` | #e2e8f0 | 邊框 (Slate 200) |
| `--color-code-bg` | #f8fafc | 程式碼區塊背景 |

### Sidebar（深色主題）

| 用途 | 值 |
|------|-----|
| 背景 | #1e293b (Slate 900) |
| 文字 | #e2e8f0 (Slate 200) |
| 邊框 | #334155 (Slate 700) |
| Hover 背景 | #334155 |
| Active 背景 | #3b82f6 (Blue 500) |
| Success 指示器 | #22c55e |

### PrimeVue 主題

- Aura preset，深色模式選擇器: `.dark-mode`

---

## 間距

常用固定值：

| 值 | 用途 |
|-----|------|
| 8px | 小間距、元素間 gap |
| 12px | 中間距、filter bar gap |
| 16px | grid gap、標準間距 |
| 20px | 卡片 padding |
| 24px | 大間距、section margin |
| 32px | 頁面 padding |
| 48px | 大區塊間距 |

佈局固定值：
- `--sidebar-width`: 260px

---

## 字型

```css
font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
```

| 元素 | 大小 | 粗細 |
|------|------|------|
| 頁面標題 (h2) | 1.5rem | 700 |
| Sidebar 標題 | 1.1rem | 700 |
| 統計數值 | 2rem | 700 |
| 表單標籤 | 0.8rem | 600 |
| 統計標籤 | 0.75rem | 600 (uppercase) |
| 預設內文 | 0.875rem | 400 |
| Sidebar 文字 | 0.875rem | 500 |
| 程式碼 | 0.8rem | 400 (monospace) |

- 行高: 1.5
- 渲染: optimizeLegibility + antialiased

---

## 圓角

| Token | 值 | 用途 |
|-------|-----|------|
| `--radius-sm` | 6px | 小按鈕、locale 切換 |
| `--radius-md` | 8px | 表單輸入、卡片 |
| `--radius-lg` | 12px | 統計卡片、對話框 |

---

## 陰影

無自定義 shadow 變數。深度透過邊框表達：
- 卡片: `1px solid var(--color-border)`
- PrimeVue 元件（Dialog, Dropdown）使用 Aura 主題自帶陰影
- Mobile overlay: `rgba(0,0,0,0.4)`

---

## 動畫

- 標準互動: `200ms ease`
- Sidebar 滑動: `transform 200ms ease`
- Hover: background + color 200ms 過渡

---

## 元件模式

### 統計卡片
```css
background: var(--color-card);
border-radius: var(--radius-lg);
padding: 20px 24px;
border: 1px solid var(--color-border);
```

### 程式碼區塊
```css
background: var(--color-code-bg);
border-radius: var(--radius-md);
padding: 12px;
font-family: monospace;
font-size: 0.8rem;
max-height: 280px;
overflow-y: auto;
border: 1px solid var(--color-border);
```

### 空狀態
```css
color: var(--color-text-muted);
padding: 24px;
text-align: center;
```

### PrimeVue 元件
- Button: severity 語意（danger=攻擊成功, success=已阻擋）
- DataTable: stripedRows + paginator, rows=20
- Tag: severity 對應狀態色
- Dialog: 480px (設定) / 800px (詳情), max-width 95vw

---

## 響應式

| 名稱 | 斷點 | 行為 |
|------|------|------|
| 桌面 | >1023px | 多欄 grid, sidebar 展開 |
| 平板 | <=1023px | Sidebar 收合為 mobile menu |
| 手機 | <=767px | 1 欄佈局 |

### Grid 系統

| Class | 桌面 | 平板 | 手機 |
|-------|------|------|------|
| `.grid-4` | 4 欄 | 2 欄 | 2 欄 |
| `.grid-2` | 2 欄 | 1 欄 | 1 欄 |
| `.grid-3` | 3 欄 | - | 1 欄 |

### Z-index
- Mobile menu button: 200
- Sidebar: 100
- Sidebar overlay: 90

---

## 色彩語意（紅隊專用）

| Severity | 意義 | 色彩 |
|----------|------|------|
| danger | 攻擊成功 | #e74c3c |
| success | 已阻擋 | #27ae60 |
| warn | 部分成功 | #f39c12 |
| info | 資訊 | #2980b9 |
