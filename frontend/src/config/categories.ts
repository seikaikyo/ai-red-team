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
      { value: 'claude-opus-4-20250514', label: 'Claude Opus 4' },
      { value: 'claude-sonnet-4-20250514', label: 'Claude Sonnet 4' },
      { value: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5' },
    ],
  },
  {
    label: 'OpenAI',
    models: [
      { value: 'gpt-4o', label: 'GPT-4o' },
      { value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
      { value: 'o3-mini', label: 'o3-mini' },
    ],
  },
  {
    label: 'Google',
    models: [
      { value: 'gemini-2.5-pro', label: 'Gemini 2.5 Pro' },
      { value: 'gemini-2.5-flash', label: 'Gemini 2.5 Flash' },
    ],
  },
  {
    label: 'Meta',
    models: [
      { value: 'llama-3.3-70b', label: 'Llama 3.3 70B' },
      { value: 'llama-3.1-8b', label: 'Llama 3.1 8B' },
    ],
  },
  {
    label: 'Mistral',
    models: [
      { value: 'mistral-large', label: 'Mistral Large' },
      { value: 'mistral-small', label: 'Mistral Small' },
    ],
  },
  {
    label: 'DeepSeek',
    models: [
      { value: 'deepseek-chat', label: 'DeepSeek V3' },
      { value: 'deepseek-reasoner', label: 'DeepSeek R1' },
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
