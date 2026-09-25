import { ref } from 'vue'
import { API_BASE } from '../config/api'
import { useApiKey } from './useApiKey'

export interface Stats {
  total_tests: number
  total_pass: number
  total_fail: number
  total_pending: number
  success_rate: number
  category_distribution: Record<string, number>
  severity_distribution: Record<string, number>
  total_templates: number
}

export function useStats() {
  const stats = ref<Stats | null>(null)
  const loading = ref(false)
  const error = ref(false)

  const { authHeaders } = useApiKey()

  async function fetchStats() {
    loading.value = true
    error.value = false
    try {
      const res = await fetch(`${API_BASE}/api/stats`, { headers: authHeaders() })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json()
      stats.value = json.data
    } catch {
      error.value = true
    } finally {
      loading.value = false
    }
  }

  return { stats, loading, error, fetchStats }
}
