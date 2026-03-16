# AI Red Team Toolkit

LLM 對抗性安全測試工具，系統化評估語言模型安全性。

## 技術架構

| 層級 | 技術 |
|------|------|
| 前端 | Vue 3 + TypeScript + PrimeVue 4 (Aura) |
| 後端 | FastAPI + SQLModel + SQLite |
| AI | Anthropic API (Claude) + OpenAI-compatible |
| 建置 | Vite 7 |
| 部署 | Vercel (前端) + Render (後端) |

## 開發指令

```bash
# 後端
cd backend && uvicorn main:app --port 8005

# 前端
cd frontend && npm run dev

# 測試
cd backend && pytest tests/ -v
cd frontend && npx vue-tsc --noEmit

# 建構
cd frontend && npm run build
```

## Port

- 前端: 5175
- 後端: 8005

## 環境變數 (Render)

- `ANTHROPIC_API_KEY` - Claude API
- `APP_API_KEY` - 應用程式認證
- `CORS_ORIGINS` - 允許的前端域名 (JSON array)
