import { ref } from 'vue'
import { API_BASE } from '../config/api'

export interface AttackTemplate {
  id: string
  name: string
  category: string
  severity: string
  description: string
  prompt_template: string
  variables: string[]
  expected_behavior: string
  tags: string[]
  language: string
  created_at: string
  updated_at: string
}

export interface TemplateForm {
  name: string
  category: string
  severity: string
  description: string
  prompt_template: string
  variables: string[]
  expected_behavior: string
  tags: string[]
  language: string
}

export function useTemplates() {
  const templates = ref<AttackTemplate[]>([])
  const loading = ref(false)

  async function fetchTemplates(params?: { category?: string; severity?: string; language?: string; q?: string }) {
    loading.value = true
    try {
      const query = new URLSearchParams()
      if (params?.category) query.set('category', params.category)
      if (params?.severity) query.set('severity', params.severity)
      if (params?.language) query.set('language', params.language)
      if (params?.q) query.set('q', params.q)
      const qs = query.toString()
      const res = await fetch(`${API_BASE}/api/templates${qs ? '?' + qs : ''}`)
      const json = await res.json()
      templates.value = json.data || []
    } finally {
      loading.value = false
    }
  }

  async function createTemplate(form: TemplateForm) {
    const res = await fetch(`${API_BASE}/api/templates`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    return (await res.json()).data as AttackTemplate
  }

  async function updateTemplate(id: string, form: Partial<TemplateForm>) {
    const res = await fetch(`${API_BASE}/api/templates/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    return (await res.json()).data as AttackTemplate
  }

  async function deleteTemplate(id: string) {
    await fetch(`${API_BASE}/api/templates/${id}`, { method: 'DELETE' })
  }

  return { templates, loading, fetchTemplates, createTemplate, updateTemplate, deleteTemplate }
}
