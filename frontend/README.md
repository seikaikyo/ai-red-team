# AI Red Team - Frontend

Vue 3 + TypeScript + PrimeVue 4 (Aura) frontend for the LLM adversarial testing toolkit.

## Setup

```bash
npm install
npm run dev -- --port 5175
```

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Dashboard | `/` | Testing overview and statistics |
| Templates | `/templates` | Manage attack prompt templates |
| Test Runner | `/runner` | Execute adversarial prompts against target models |
| Results | `/results` | Review test results and verdicts |
| Report | `/report` | Export Markdown reports |

## i18n

Trilingual UI with English, Traditional Chinese, and Japanese. Language preference persisted via localStorage.

## Build

```bash
npm run build
```

Output directory: `dist/`
