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

router.afterEach((to) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - AI Red Team Toolkit` : 'AI Red Team Toolkit'
})

export default router
