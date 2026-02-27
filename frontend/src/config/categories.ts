export const CATEGORIES = [
  { value: 'prompt_injection', label: 'Prompt Injection', icon: 'pi pi-code', color: '#e74c3c' },
  { value: 'jailbreak', label: 'Jailbreak', icon: 'pi pi-lock-open', color: '#e67e22' },
  { value: 'bias', label: 'Bias Detection', icon: 'pi pi-users', color: '#9b59b6' },
  { value: 'safety_bypass', label: 'Safety Bypass', icon: 'pi pi-shield', color: '#c0392b' },
  { value: 'multilingual', label: 'Multilingual', icon: 'pi pi-globe', color: '#2980b9' },
] as const

export const SEVERITIES = [
  { value: 'low', label: 'Low', color: '#27ae60' },
  { value: 'medium', label: 'Medium', color: '#f39c12' },
  { value: 'high', label: 'High', color: '#e67e22' },
  { value: 'critical', label: 'Critical', color: '#e74c3c' },
] as const

export const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'zh', label: 'Chinese' },
  { value: 'mixed', label: 'Mixed' },
] as const

export const MODELS = [
  { value: 'claude-sonnet-4-20250514', label: 'Claude Sonnet 4' },
  { value: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5' },
  { value: 'claude-opus-4-20250514', label: 'Claude Opus 4' },
] as const

export type Category = typeof CATEGORIES[number]['value']
export type Severity = typeof SEVERITIES[number]['value']
