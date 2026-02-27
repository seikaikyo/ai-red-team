<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import Select from 'primevue/select'
import Textarea from 'primevue/textarea'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
import { CATEGORIES } from '../config/categories'
import { generateReport, downloadMarkdown } from '../utils/report-export'

const { results, fetchResults } = useTestRunner()
const categoryFilter = ref<string | null>(null)
const verdictFilter = ref<string | null>(null)

const filteredResults = computed(() => {
  let data = results.value
  if (categoryFilter.value) data = data.filter(r => r.category === categoryFilter.value)
  if (verdictFilter.value === 'true') data = data.filter(r => r.success === true)
  if (verdictFilter.value === 'false') data = data.filter(r => r.success === false)
  if (verdictFilter.value === 'null') data = data.filter(r => r.success === null)
  return data
})

const reportContent = computed(() => generateReport(filteredResults.value))

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
        <h2>Report Export</h2>
        <p>Generate and download Markdown reports</p>
      </div>
      <Button label="Download .md" icon="pi pi-download" :disabled="!filteredResults.length" @click="doExport" />
    </div>
  </div>

  <div style="display: flex; gap: 12px; margin-bottom: 16px">
    <Select
      v-model="categoryFilter"
      :options="[{ value: null, label: 'All Categories' }, ...CATEGORIES]"
      optionLabel="label"
      optionValue="value"
      placeholder="Category"
      showClear
      style="width: 200px"
    />
    <Select
      v-model="verdictFilter"
      :options="[
        { value: null, label: 'All Verdicts' },
        { value: 'true', label: 'Pass (Exploited)' },
        { value: 'false', label: 'Fail (Blocked)' },
        { value: 'null', label: 'Pending' },
      ]"
      optionLabel="label"
      optionValue="value"
      placeholder="Verdict"
      showClear
      style="width: 200px"
    />
    <span style="color: #64748b; align-self: center; font-size: 0.875rem">
      {{ filteredResults.length }} result(s) selected
    </span>
  </div>

  <div class="stat-card">
    <div style="font-weight: 600; margin-bottom: 12px">Preview</div>
    <pre style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; font-size: 0.8rem; white-space: pre-wrap; max-height: 600px; overflow-y: auto; font-family: monospace">{{ reportContent || 'No results to report. Run some tests first.' }}</pre>
  </div>
</template>
