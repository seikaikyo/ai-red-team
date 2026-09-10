import { createApp } from 'vue'
import * as Sentry from '@sentry/vue'
import { inject } from '@vercel/analytics'
import { injectSpeedInsights } from '@vercel/speed-insights'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'
import 'primeicons/primeicons.css'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const sentryDsn = import.meta.env.VITE_SENTRY_DSN
if (sentryDsn) {
  Sentry.init({
    app,
    dsn: sentryDsn,
    environment: import.meta.env.MODE,
    integrations: [Sentry.browserTracingIntegration({ router })],
    tracesSampleRate: 0.2,
    replaysSessionSampleRate: 0,
    replaysOnErrorSampleRate: 0,
    sendDefaultPii: false,
    // 瀏覽器擴充套件注入的雜訊，不是這個站的程式碼。微軟 Office 系套件會丟出
    // 一個不是 Error 的字串、沒有 stack，例如
    //   Object Not Found Matching Id:1, MethodName:update, ParamCount:4
    // 每個裝了那個套件的訪客都會產生一筆，會把真訊號淹掉。
    beforeSend(event, hint) {
      const raw = hint?.originalException
      const text =
        typeof raw === 'string' ? raw : (event.exception?.values?.[0]?.value ?? '')
      if (/Object Not Found Matching Id:\d+/.test(text)) return null
      return event
    },
  })
}

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.dark-mode',
    },
  },
})
app.use(ToastService)
app.use(ConfirmationService)
app.use(router)
app.directive('tooltip', Tooltip)

app.mount('#app')

inject()
injectSpeedInsights()
