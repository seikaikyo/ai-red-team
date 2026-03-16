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

  <div v-if="loading" class="loading-state" role="status" aria-live="polite">{{ t('dashboard.loading') }}</div>

  <template v-else-if="stats">
    <div class="grid-4" role="region" :aria-label="t('dashboard.title')">
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

    <div class="grid-2">
      <div class="stat-card">
        <div class="card-title">{{ t('dashboard.byCategory') }}</div>
        <div
          v-for="(count, cat) in stats.category_distribution"
          :key="cat"
          class="distribution-row"
        >
          <Tag :value="categoryLabel(String(cat))" severity="info" />
          <span class="distribution-count">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.category_distribution).length === 0" class="empty-state">
          {{ t('dashboard.noData') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="card-title">{{ t('dashboard.bySeverity') }}</div>
        <div
          v-for="(count, sev) in stats.severity_distribution"
          :key="sev"
          class="distribution-row"
        >
          <span style="text-transform: capitalize">{{ t(`severity.${sev}`) }}</span>
          <span class="distribution-count">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.severity_distribution).length === 0" class="empty-state">
          {{ t('dashboard.noData') }}
        </div>
      </div>
    </div>

    <div class="stat-card" style="margin-top: 24px">
      <div class="label">{{ t('dashboard.templatesInLibrary') }}</div>
      <div class="value">{{ stats.total_templates }}</div>
    </div>
  </template>

  <div v-else class="empty-state" style="padding: 48px">
    {{ t('dashboard.empty') }}
  </div>
</template>
