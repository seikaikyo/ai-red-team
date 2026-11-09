import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { title: 'Dashboard' },
    },
    {
      path: '/templates',
      name: 'templates',
      component: () => import('../views/TemplatesView.vue'),
      meta: { title: 'Templates' },
    },
    {
      path: '/runner',
      name: 'runner',
      component: () => import('../views/RunnerView.vue'),
      meta: { title: 'Test Runner' },
    },
    {
      path: '/results',
      name: 'results',
      component: () => import('../views/ResultsView.vue'),
      meta: { title: 'Results' },
    },
    {
      path: '/report',
      name: 'report',
      component: () => import('../views/ReportView.vue'),
      meta: { title: 'Report' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { title: '404' },
    },
  ],
})

// 部署新版後舊檔名會被換掉，開著舊分頁的人切頁會載不到程式檔，畫面空白。
// 遇到這種錯誤就重新整理一次載入新版；10 秒內不重複，避免檔案真的不見時無限重整。
const CHUNK_LOAD_ERROR =
  /Failed to fetch dynamically imported module|Importing a module script failed|error loading dynamically imported module/i
router.onError((err, to) => {
  if (!CHUNK_LOAD_ERROR.test(err instanceof Error ? err.message : String(err))) return
  try {
    const last = Number(sessionStorage.getItem('chunk-reload-at')) || 0
    if (Date.now() - last < 10_000) return
    sessionStorage.setItem('chunk-reload-at', String(Date.now()))
  } catch {
    return
  }
  window.location.assign(to.fullPath)
})

router.afterEach((to) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - AI Red Team Toolkit` : 'AI Red Team Toolkit'
})

export default router
