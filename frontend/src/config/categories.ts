export const CATEGORIES = [
  { value: 'prompt_injection', labelKey: 'category.prompt_injection', label: 'Prompt Injection', icon: 'pi pi-code', color: '#e74c3c' },
  { value: 'jailbreak', labelKey: 'category.jailbreak', label: 'Jailbreak', icon: 'pi pi-lock-open', color: '#e67e22' },
  { value: 'bias', labelKey: 'category.bias', label: 'Bias Detection', icon: 'pi pi-users', color: '#9b59b6' },
  { value: 'safety_bypass', labelKey: 'category.safety_bypass', label: 'Safety Bypass', icon: 'pi pi-shield', color: '#c0392b' },
  { value: 'multilingual', labelKey: 'category.multilingual', label: 'Multilingual', icon: 'pi pi-globe', color: '#2980b9' },
  { value: 'tool_use', labelKey: 'category.tool_use', label: 'Tool Use Injection', icon: 'pi pi-wrench', color: '#e91e63' },
  { value: 'multi_turn', labelKey: 'category.multi_turn', label: 'Multi-turn Attack', icon: 'pi pi-comments', color: '#ff5722' },
  { value: 'rag_poisoning', labelKey: 'category.rag_poisoning', label: 'RAG Poisoning', icon: 'pi pi-database', color: '#795548' },
  { value: 'output_manipulation', labelKey: 'category.output_manipulation', label: 'Output Manipulation', icon: 'pi pi-file-export', color: '#607d8b' },
  { value: 'system_prompt_reconstruction', labelKey: 'category.system_prompt_reconstruction', label: 'System Prompt Recon', icon: 'pi pi-search', color: '#3f51b5' },
  { value: 'hallucination', labelKey: 'category.hallucination', label: 'Hallucination', icon: 'pi pi-exclamation-circle', color: '#ff9800' },
  { value: 'training_data_extraction', labelKey: 'category.training_data_extraction', label: 'Training Data Extract', icon: 'pi pi-download', color: '#f44336' },
] as const

export const SEVERITIES = [
  { value: 'low', labelKey: 'severity.low', label: 'Low', color: '#27ae60' },
  { value: 'medium', labelKey: 'severity.medium', label: 'Medium', color: '#f39c12' },
  { value: 'high', labelKey: 'severity.high', label: 'High', color: '#e67e22' },
  { value: 'critical', labelKey: 'severity.critical', label: 'Critical', color: '#e74c3c' },
] as const

export const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'zh', label: 'Chinese' },
  { value: 'ja', label: 'Japanese' },
  { value: 'mixed', label: 'Mixed' },
] as const

export const MODEL_GROUPS = [
  {
    label: 'Anthropic',
    models: [
      { value: 'claude-opus-4-8', label: 'Opus 4.8' },
      { value: 'claude-sonnet-5', label: 'Sonnet 5' },
      { value: 'claude-haiku-4-5-20251001', label: 'Haiku 4.5' },
      { value: 'claude-fable-5', label: 'Fable 5' },
    ],
  },
  {
    label: 'OpenAI',
    models: [
      { value: 'gpt-5.5', label: 'GPT-5.5' },
      { value: 'gpt-5.4-mini', label: 'GPT-5.4 Mini' },
      { value: 'gpt-5.4-nano', label: 'GPT-5.4 Nano' },
    ],
  },
  {
    label: 'Google',
    models: [
      { value: 'gemini-3-pro-preview', label: 'Gemini 3 Pro' },
      { value: 'gemini-3-flash-preview', label: 'Gemini 3 Flash' },
    ],
  },
  {
    label: 'xAI',
    models: [
      { value: 'grok-4.3', label: 'Grok 4.3' },
    ],
  },
  {
    label: 'Meta',
    models: [
      { value: 'Llama-4-Maverick-17B-128E-Instruct-FP8', label: 'Llama 4 Maverick' },
      { value: 'Llama-4-Scout-17B-16E-Instruct-FP8', label: 'Llama 4 Scout' },
    ],
  },
  {
    label: 'Mistral',
    models: [
      { value: 'mistral-large-latest', label: 'Large 3' },
      { value: 'mistral-small-latest', label: 'Small 4' },
    ],
  },
  {
    label: 'DeepSeek',
    models: [
      { value: 'deepseek-v4-pro', label: 'V4 Pro' },
      { value: 'deepseek-v4-flash', label: 'V4 Flash' },
    ],
  },
] as const

// Flat model list for backward compatibility
export const MODELS = MODEL_GROUPS.flatMap(g =>
  g.models.map(m => ({ ...m, provider: g.label.toLowerCase() as string }))
)

export const CUSTOM_PROVIDER_PRESETS = [
  { value: 'ollama', label: 'Ollama', defaultUrl: 'http://localhost:11434/v1' },
  { value: 'vllm', label: 'vLLM', defaultUrl: 'http://localhost:8000/v1' },
  { value: 'lmstudio', label: 'LM Studio', defaultUrl: 'http://localhost:1234/v1' },
  { value: 'custom', label: 'Custom', defaultUrl: '' },
] as const

export type ProviderPreset = typeof CUSTOM_PROVIDER_PRESETS[number]['value']

export type Category = typeof CATEGORIES[number]['value']
export type Severity = typeof SEVERITIES[number]['value']
