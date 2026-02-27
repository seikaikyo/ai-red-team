<script setup lang="ts">
import { onMounted } from 'vue'
import Tag from 'primevue/tag'
import { useStats } from '../composables/useStats'
import { CATEGORIES } from '../config/categories'

const { stats, loading, fetchStats } = useStats()

onMounted(() => fetchStats())

function categoryLabel(key: string) {
  return CATEGORIES.find(c => c.value === key)?.label || key
}
</script>

<template>
  <div class="page-header">
    <h2>Dashboard</h2>
    <p>Testing overview and statistics</p>
  </div>

  <div v-if="loading" style="text-align: center; padding: 48px; color: #94a3b8">Loading...</div>

  <template v-else-if="stats">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px">
      <div class="stat-card">
        <div class="label">Total Tests</div>
        <div class="value">{{ stats.total_tests }}</div>
      </div>
      <div class="stat-card">
        <div class="label">Attack Success</div>
        <div class="value" style="color: var(--color-danger)">{{ stats.total_pass }}</div>
      </div>
      <div class="stat-card">
        <div class="label">Blocked</div>
        <div class="value" style="color: var(--color-success)">{{ stats.total_fail }}</div>
      </div>
      <div class="stat-card">
        <div class="label">Success Rate</div>
        <div class="value">{{ stats.success_rate.toFixed(1) }}%</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
      <div class="stat-card">
        <div class="label" style="margin-bottom: 16px">By Category</div>
        <div v-for="(count, cat) in stats.category_distribution" :key="cat"
          style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9">
          <Tag :value="categoryLabel(String(cat))" severity="info" />
          <span style="font-weight: 600">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.category_distribution).length === 0" style="color: #94a3b8; padding: 12px 0">
          No test data yet
        </div>
      </div>
      <div class="stat-card">
        <div class="label" style="margin-bottom: 16px">By Severity</div>
        <div v-for="(count, sev) in stats.severity_distribution" :key="sev"
          style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9">
          <span style="text-transform: capitalize">{{ sev }}</span>
          <span style="font-weight: 600">{{ count }}</span>
        </div>
        <div v-if="Object.keys(stats.severity_distribution).length === 0" style="color: #94a3b8; padding: 12px 0">
          No test data yet
        </div>
      </div>
    </div>

    <div class="stat-card" style="margin-top: 24px">
      <div class="label">Templates in Library</div>
      <div class="value">{{ stats.total_templates }}</div>
    </div>
  </template>

  <div v-else style="text-align: center; padding: 48px; color: #94a3b8">
    No data available. Run some tests to see statistics.
  </div>
</template>
