import { ref } from 'vue'
import { API_BASE } from '../config/api'

export interface TestRun {
  id: string
  template_id: string
  template_name: string
  model: string
  prompt_sent: string
  response: string
  success: boolean | null
  notes: string
  duration_ms: number
  category: string
  severity: string
  created_at: string
}

export interface RunRequest {
  template_id: string
  model: string
  variables: Record<string, string>
  max_tokens: number
  temperature: number
  base_url?: string | null
}

export function useTestRunner() {
  const results = ref<TestRun[]>([])
  const running = ref(false)
  const loading = ref(false)

  async function runTest(req: RunRequest): Promise<TestRun> {
    running.value = true
    try {
      const res = await fetch(`${API_BASE}/api/tests/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
      })
      const json = await res.json()
      if (!json.success) throw new Error(json.error?.message || 'Test failed')
      return json.data as TestRun
    } finally {
      running.value = false
    }
  }

  async function fetchResults(params?: { category?: string; success?: string }) {
    loading.value = true
    try {
      const query = new URLSearchParams()
      if (params?.category) query.set('category', params.category)
      if (params?.success) query.set('success', params.success)
      const qs = query.toString()
      const res = await fetch(`${API_BASE}/api/tests${qs ? '?' + qs : ''}`)
      const json = await res.json()
      results.value = json.data || []
    } finally {
      loading.value = false
    }
  }

  async function updateVerdict(id: string, success: boolean | null, notes: string = '') {
    const res = await fetch(`${API_BASE}/api/tests/${id}/verdict`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success, notes }),
    })
    return (await res.json()).data as TestRun
  }

  return { results, running, loading, runTest, fetchResults, updateVerdict }
}
