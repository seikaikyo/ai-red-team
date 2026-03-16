import { ref, computed } from 'vue'

const STORAGE_KEY = 'redteam_api_key'

const apiKey = ref(sessionStorage.getItem(STORAGE_KEY) || '')

function setApiKey(key: string) {
  apiKey.value = key
  if (key) {
    sessionStorage.setItem(STORAGE_KEY, key)
  } else {
    sessionStorage.removeItem(STORAGE_KEY)
  }
}

const hasApiKey = computed(() => apiKey.value.length > 0)

function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (apiKey.value) {
    headers['X-API-Key'] = apiKey.value
  }
  return headers
}

export function useApiKey() {
  return { apiKey, hasApiKey, setApiKey, authHeaders }
}
