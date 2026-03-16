<script setup lang="ts">
import Button from 'primevue/button'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
</script>

<template>
  <div class="not-found">
    <h1>404</h1>
    <p>{{ t('common.pageNotFound') }}</p>
    <router-link to="/">
      <Button :label="t('common.backToDashboard')" icon="pi pi-arrow-left" />
    </router-link>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  gap: 16px;
}

.not-found h1 {
  font-size: 4rem;
  font-weight: 800;
  color: #cbd5e1;
}

.not-found p {
  font-size: 1.125rem;
  color: #64748b;
}
</style>
