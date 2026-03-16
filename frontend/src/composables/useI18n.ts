import { ref, computed } from 'vue'
import en from '../config/i18n/en'
import zh from '../config/i18n/zh'
import ja from '../config/i18n/ja'

export type Locale = 'en' | 'zh' | 'ja'

const messages: Record<Locale, Record<string, string>> = { en, zh, ja }

function detectLocale(): Locale {
  const saved = localStorage.getItem('locale') as Locale
  if (saved && saved in messages) return saved
  const lang = navigator.language.toLowerCase()
  if (lang.startsWith('zh')) return 'zh'
  if (lang.startsWith('ja')) return 'ja'
  return 'en'
}

const locale = ref<Locale>(detectLocale())

function setLocale(l: Locale) {
  locale.value = l
  localStorage.setItem('locale', l)
}

function t(key: string, params?: Record<string, string | number>): string {
  let text = messages[locale.value][key] || messages.en[key] || key
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      text = text.replaceAll(`{{${k}}}`, String(v))
    }
  }
  return text
}

const localeLabel = computed(() => {
  const labels: Record<Locale, string> = { en: 'EN', zh: '中', ja: '日' }
  return labels[locale.value]
})

export function useI18n() {
  return { locale, setLocale, t, localeLabel }
}
