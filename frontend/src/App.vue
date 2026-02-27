<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useI18n, type Locale } from './composables/useI18n'

const router = useRouter()
const { t, locale, setLocale } = useI18n()

const navItems = computed(() => [
  { label: t('nav.dashboard'), icon: 'pi pi-chart-bar', to: '/' },
  { label: t('nav.templates'), icon: 'pi pi-file-edit', to: '/templates' },
  { label: t('nav.runner'), icon: 'pi pi-play', to: '/runner' },
  { label: t('nav.results'), icon: 'pi pi-list', to: '/results' },
  { label: t('nav.report'), icon: 'pi pi-download', to: '/report' },
])

const locales: { value: Locale; label: string }[] = [
  { value: 'en', label: 'EN' },
  { value: 'zh', label: '中' },
  { value: 'ja', label: '日' },
]
</script>

<template>
  <Toast />
  <ConfirmDialog />

  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>{{ t('app.title') }}</h1>
      <p>{{ t('app.subtitle') }}</p>
    </div>
    <nav class="sidebar-nav">
      <router-link v-for="item in navItems" :key="item.to" :to="item.to">
        <i :class="item.icon"></i>
        {{ item.label }}
      </router-link>
    </nav>
    <div class="sidebar-locale">
      <button
        v-for="l in locales"
        :key="l.value"
        :class="['locale-btn', { active: locale === l.value }]"
        @click="setLocale(l.value)"
      >
        {{ l.label }}
      </button>
    </div>
  </aside>

  <main class="main-content">
    <router-view />
  </main>
</template>
