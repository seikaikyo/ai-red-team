# AI Red Team Toolkit

LLM adversarial testing toolkit for systematically evaluating language model safety. Supports prompt injection, jailbreak, bias detection, safety bypass, and multilingual attack vectors.

## Disclaimer

This toolkit is intended **solely for authorized security testing, academic research, and defensive AI safety evaluation**. The attack templates included are designed to identify vulnerabilities in LLM safety mechanisms so they can be strengthened.

- Do NOT use this toolkit to attack production systems without explicit authorization
- Do NOT use the attack templates to generate harmful content
- The authors assume no liability for misuse of this software
- All testing should comply with applicable laws, regulations, and the target model provider's terms of service

## Features

- **96 attack templates** across 5 categories (EN / ZH / JA)
- **Test runner** with variable substitution and model configuration
- **Result tracking** with manual verdict (Pass / Fail / Pending)
- **Markdown report export** with per-category breakdown
- **Trilingual UI** (English, Traditional Chinese, Japanese) with localStorage persistence

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + TypeScript + PrimeVue 4 (Aura) |
| Backend | FastAPI + SQLModel + SQLite |
| AI | Anthropic API (Claude) |
| Build | Vite 7 |

## Quick Start

### Prerequisites

- Node.js >= 20
- Python >= 3.11
- Anthropic API key

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env

uvicorn main:app --port 8005
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --port 5174
```

Open http://localhost:5174

## Attack Categories

| Category | Templates | Description |
|----------|:---------:|-------------|
| Prompt Injection | 8 x 3 | System prompt extraction, instruction override, delimiter injection |
| Jailbreak | 8 x 3 | DAN, roleplay, hypothetical framing, token smuggling |
| Bias Detection | 6 x 3 | Gender, race, age, socioeconomic, disability bias |
| Safety Bypass | 5 x 3 | Tutorial framing, medical misinfo, PII generation, malware |
| Multilingual | 5 x 3 | Language switching, translation bypass, code-mixing |

Each category has English, Traditional Chinese, and Japanese variants for cross-language safety evaluation.

## Project Structure

```
ai-red-team/
  backend/
    main.py              # FastAPI app + CORS
    models.py            # SQLModel schema
    config.py            # Settings (env-based)
    database.py          # DB init + seed loader
    routers/
      templates.py       # Template CRUD API
      tests.py           # Test execution API
      stats.py           # Statistics API
    services/
      runner.py          # Anthropic API test runner
    seed/
      templates.json     # 96 attack templates (EN/ZH/JA)
  frontend/
    src/
      views/             # 5 pages: Dashboard, Templates, Runner, Results, Report
      composables/       # useTemplates, useTestRunner, useStats, useI18n
      config/
        categories.ts    # Attack categories + severities
        i18n/            # EN / ZH / JA translations
      utils/
        report-export.ts # Markdown report generator
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/templates` | List all templates |
| POST | `/templates` | Create template |
| PUT | `/templates/{id}` | Update template |
| DELETE | `/templates/{id}` | Delete template |
| POST | `/tests/run` | Execute a test against target model |
| GET | `/tests` | List test results |
| PATCH | `/tests/{id}/verdict` | Update test verdict |
| GET | `/stats` | Dashboard statistics |
| GET | `/health` | Health check |

## License

MIT
