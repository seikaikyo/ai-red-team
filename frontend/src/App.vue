<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useI18n, type Locale } from './composables/useI18n'

const { t, locale, setLocale } = useI18n()
const route = useRoute()
const sidebarOpen = ref(false)

const navItems = computed(() => [
  { label: t('nav.dashboard'), icon: 'pi pi-chart-bar', to: '/' },
  { label: t('nav.templates'), icon: 'pi pi-file-edit', to: '/templates' },
  { label: t('nav.runner'), icon: 'pi pi-play', to: '/runner' },
  { label: t('nav.results'), icon: 'pi pi-list', to: '/results' },
  { label: t('nav.report'), icon: 'pi pi-download', to: '/report' },
])

const locales: { value: Locale; label: string; ariaLabel: string }[] = [
  { value: 'en', label: 'EN', ariaLabel: 'Switch to English' },
  { value: 'zh', label: '中', ariaLabel: 'Switch to Chinese' },
  { value: 'ja', label: '日', ariaLabel: 'Switch to Japanese' },
]

watch(route, () => {
  sidebarOpen.value = false
})

watch(locale, (val) => {
  document.documentElement.lang = val === 'zh' ? 'zh-Hant' : val
})
</script>

<template>
  <Toast />
  <ConfirmDialog />

  <button
    class="mobile-menu-btn"
    :aria-label="t('common.toggleMenu')"
    aria-expanded="false"
    @click="sidebarOpen = !sidebarOpen"
  >
    <i :class="sidebarOpen ? 'pi pi-times' : 'pi pi-bars'"></i>
  </button>

  <div
    class="sidebar-overlay"
    :class="{ visible: sidebarOpen }"
    @click="sidebarOpen = false"
  ></div>

  <aside class="sidebar" :class="{ open: sidebarOpen }" role="navigation" :aria-label="t('common.mainNav')">
    <div class="sidebar-header">
      <h1>{{ t('app.title') }}</h1>
      <p>{{ t('app.subtitle') }}</p>
    </div>
    <nav class="sidebar-nav" :aria-label="t('common.pageNav')">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        :aria-current="route.path === item.to ? 'page' : undefined"
      >
        <i :class="item.icon" aria-hidden="true"></i>
        {{ item.label }}
      </router-link>
    </nav>
    <div class="sidebar-locale" role="group" :aria-label="t('common.langSwitch')">
      <button
        v-for="l in locales"
        :key="l.value"
        :class="['locale-btn', { active: locale === l.value }]"
        :aria-label="l.ariaLabel"
        :aria-pressed="locale === l.value"
        @click="setLocale(l.value)"
      >
        {{ l.label }}
      </button>
    </div>
  </aside>

  <main class="main-content" role="main">
    <router-view />
  </main>
</template>
