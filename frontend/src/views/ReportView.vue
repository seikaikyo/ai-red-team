<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import Select from 'primevue/select'
import { useTestRunner } from '../composables/useTestRunner'
import { CATEGORIES } from '../config/categories'
import { generateReport, downloadMarkdown } from '../utils/report-export'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const { results, fetchResults } = useTestRunner()
const categoryFilter = ref<string | null>(null)
const verdictFilter = ref<string | null>(null)

const i18nCategories = computed(() =>
  CATEGORIES.map(c => ({ ...c, label: t(c.labelKey) }))
)

const filteredResults = computed(() => {
  let data = results.value
  if (categoryFilter.value) data = data.filter(r => r.category === categoryFilter.value)
  if (verdictFilter.value === 'true') data = data.filter(r => r.success === true)
  if (verdictFilter.value === 'false') data = data.filter(r => r.success === false)
  if (verdictFilter.value === 'null') data = data.filter(r => r.success === null)
  return data
})

const reportContent = computed(() => generateReport(filteredResults.value, t))

function doExport() {
  const model = filteredResults.value[0]?.model || 'unknown'
  const date = new Date().toISOString().slice(0, 10)
  downloadMarkdown(reportContent.value, `report-${model.replace('claude-', '')}-${date}.md`)
}

onMounted(() => fetchResults())
</script>

<template>
  <div class="page-header">
    <div class="page-header-row">
      <div>
        <h2>{{ t('report.title') }}</h2>
        <p>{{ t('report.subtitle') }}</p>
      </div>
      <Button :label="t('report.downloadBtn')" icon="pi pi-download" :disabled="!filteredResults.length" @click="doExport" />
    </div>
  </div>

  <div class="filter-bar">
    <Select
      v-model="categoryFilter"
      :options="[{ value: null, label: t('report.allCategories') }, ...i18nCategories]"
      optionLabel="label"
      optionValue="value"
      :placeholder="t('report.allCategories')"
      showClear
      style="width: 200px"
      :aria-label="t('results.category')"
    />
    <Select
      v-model="verdictFilter"
      :options="[
        { value: null, label: t('report.allVerdicts') },
        { value: 'true', label: t('report.passExploited') },
        { value: 'false', label: t('report.failBlocked') },
        { value: 'null', label: t('report.pending') },
      ]"
      optionLabel="label"
      optionValue="value"
      :placeholder="t('report.allVerdicts')"
      showClear
      style="width: 200px"
      :aria-label="t('results.verdict')"
    />
    <span class="result-info">
      {{ t('report.resultsSelected', { count: filteredResults.length }) }}
    </span>
  </div>

  <div class="stat-card">
    <div class="card-title">{{ t('report.preview') }}</div>
    <pre class="report-preview">{{ reportContent || t('report.empty') }}</pre>
  </div>
</template>
