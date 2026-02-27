<script setup lang="ts">
import { onMounted } from 'vue'
import Tag from 'primevue/tag'
import { useStats } from '../composables/useStats'
import { CATEGORIES } from '../config/categories'
import { useI18n } from '../composables/useI18n'

const { stats, loading, fetchStats } = useStats()
const { t } = useI18n()

onMounted(() => fetchStats())

function categoryLabel(key: string) {
  const cat = CATEGORIES.find(c => c.value === key)
  return cat ? t(cat.labelKey) : key
}
</script>

<template>
  <div class="page-header">
    <h2>{{ t('dashboard.title') }}</h2>
    <p>{{ t('dashboard.subtitle') }}</p>
  </div>

  <div v-if="loading" style="text-align: center; padding: 48px; color: #94a3b8">{{ t('dashboard.loading') }}</div>

  <template v-else-if="stats">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px">
      <div class="stat-card">
        <div class="label">{{ t('dashboard.totalTests') }}</div>
        <div class="value">{{ stats.total_tests }}</div>
      </div>
      <div class="stat-card">
        <div class="label">{{ t('dashboard.attackSuccess') }}</div>
        <div class="value" style="color: var(--color-danger)">{{ stats.total_pass }}</div>
      </div>
      <div class="stat-card">
        <div class="label">{{ t('dashboard.blocked') }}</div>
        <div class="value" style="color: var(--color-success)">{{ stats.total_fail }}</div>
      </div>
      <div class="stat-card">
        <div class="label">{{ t('dashboard.successRate') }}</div>
        <div class="value">{{ stats.success_rate.toFixed(1) }}%</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
      <div class="stat-card">
        <div class="label" style="margin-bottom: 16px">{{ t('dashboard.byCategory') }}</div>
        <div v-for="(count, cat) in stats.category_distribution" :key="cat"
          style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9">
          <Tag :value="categoryLabel(String(cat))" severity="info" />
          <span style="font-weight: 600">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.category_distribution).length === 0" style="color: #94a3b8; padding: 12px 0">
          {{ t('dashboard.noData') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="label" style="margin-bottom: 16px">{{ t('dashboard.bySeverity') }}</div>
        <div v-for="(count, sev) in stats.severity_distribution" :key="sev"
          style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9">
          <span style="text-transform: capitalize">{{ t(`severity.${sev}`) }}</span>
          <span style="font-weight: 600">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.severity_distribution).length === 0" style="color: #94a3b8; padding: 12px 0">
          {{ t('dashboard.noData') }}
        </div>
      </div>
    </div>

    <div class="stat-card" style="margin-top: 24px">
      <div class="label">{{ t('dashboard.templatesInLibrary') }}</div>
      <div class="value">{{ stats.total_templates }}</div>
    </div>
  </template>

  <div v-else style="text-align: center; padding: 48px; color: #94a3b8">
    {{ t('dashboard.empty') }}
  </div>
</template>
