<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import Select from 'primevue/select'
import Textarea from 'primevue/textarea'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
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
    <div style="display: flex; justify-content: space-between; align-items: center">
      <div>
        <h2>{{ t('report.title') }}</h2>
        <p>{{ t('report.subtitle') }}</p>
      </div>
      <Button :label="t('report.downloadBtn')" icon="pi pi-download" :disabled="!filteredResults.length" @click="doExport" />
    </div>
  </div>

  <div style="display: flex; gap: 12px; margin-bottom: 16px">
    <Select
      v-model="categoryFilter"
      :options="[{ value: null, label: t('report.allCategories') }, ...i18nCategories]"
      optionLabel="label"
      optionValue="value"
      placeholder="Category"
      showClear
      style="width: 200px"
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
      placeholder="Verdict"
      showClear
      style="width: 200px"
    />
    <span style="color: #64748b; align-self: center; font-size: 0.875rem">
      {{ t('report.resultsSelected', { count: filteredResults.length }) }}
    </span>
  </div>

  <div class="stat-card">
    <div style="font-weight: 600; margin-bottom: 12px">{{ t('report.preview') }}</div>
    <pre style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; font-size: 0.8rem; white-space: pre-wrap; max-height: 600px; overflow-y: auto; font-family: monospace">{{ reportContent || t('report.empty') }}</pre>
  </div>
</template>
