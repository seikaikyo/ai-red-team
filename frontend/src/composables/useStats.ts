import { ref } from 'vue'
import { API_BASE } from '../config/api'

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

  async function fetchStats() {
    loading.value = true
    try {
      const res = await fetch(`${API_BASE}/api/stats`)
      const json = await res.json()
      stats.value = json.data
    } finally {
      loading.value = false
    }
  }

  return { stats, loading, fetchStats }
}
