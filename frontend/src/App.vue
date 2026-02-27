<script setup lang="ts">
import { useRouter } from 'vue-router'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'

const router = useRouter()

const navItems = [
  { label: 'Dashboard', icon: 'pi pi-chart-bar', to: '/' },
  { label: 'Templates', icon: 'pi pi-file-edit', to: '/templates' },
  { label: 'Test Runner', icon: 'pi pi-play', to: '/runner' },
  { label: 'Results', icon: 'pi pi-list', to: '/results' },
  { label: 'Report', icon: 'pi pi-download', to: '/report' },
]
</script>

<template>
  <Toast />
  <ConfirmDialog />

  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>AI Red Team</h1>
      <p>LLM Adversarial Testing</p>
    </div>
    <nav class="sidebar-nav">
      <router-link v-for="item in navItems" :key="item.to" :to="item.to">
        <i :class="item.icon"></i>
        {{ item.label }}
      </router-link>
    </nav>
  </aside>

  <main class="main-content">
    <router-view />
  </main>
</template>
