<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
import { CATEGORIES } from '../config/categories'
import { useI18n } from '../composables/useI18n'

const toast = useToast()
const { t } = useI18n()
const { results, loading, fetchResults, updateVerdict } = useTestRunner()

const detailVisible = ref(false)
const detailItem = ref<TestRun | null>(null)
const categoryFilter = ref<string | null>(null)
const successFilter = ref<string | null>(null)

const i18nCategories = computed(() =>
  CATEGORIES.map(c => ({ ...c, label: t(c.labelKey) }))
)

function showDetail(item: TestRun) {
  detailItem.value = item
  detailVisible.value = true
}

async function setVerdict(item: TestRun, success: boolean | null) {
  try {
    await updateVerdict(item.id, success)
    item.success = success
    toast.add({ severity: 'success', summary: t('results.verdictUpdated'), life: 2000 })
  } catch (e: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: e.message })
  }
}

function verdictSeverity(s: boolean | null) {
  if (s === true) return 'danger'
  if (s === false) return 'success'
  return 'warn'
}

function verdictLabel(s: boolean | null) {
  if (s === true) return t('results.passExploited')
  if (s === false) return t('results.failBlocked')
  return t('results.pending')
}

function formatDate(d: string) {
  return new Date(d).toLocaleString('zh-TW', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function reload() {
  fetchResults({
    category: categoryFilter.value || undefined,
    success: successFilter.value ?? undefined,
  })
}

onMounted(() => fetchResults())
</script>

<template>
  <div class="page-header">
    <h2>{{ t('results.title') }}</h2>
    <p>{{ t('results.subtitle') }}</p>
  </div>

  <div style="display: flex; gap: 12px; margin-bottom: 16px">
    <Select
      v-model="categoryFilter"
      :options="[{ value: null, label: t('results.allCategories') }, ...i18nCategories]"
      optionLabel="label"
      optionValue="value"
      placeholder="Category"
      showClear
      style="width: 200px"
      @change="reload"
    />
    <Select
      v-model="successFilter"
      :options="[
        { value: null, label: t('results.allVerdicts') },
        { value: 'true', label: t('results.passExploited') },
        { value: 'false', label: t('results.failBlocked') },
        { value: 'null', label: t('results.pending') },
      ]"
      optionLabel="label"
      optionValue="value"
      placeholder="Verdict"
      showClear
      style="width: 200px"
      @change="reload"
    />
  </div>

  <DataTable
    :value="results"
    :loading="loading"
    stripedRows
    paginator
    :rows="20"
    dataKey="id"
    style="background: #fff; border-radius: 12px; border: 1px solid #e2e8f0"
  >
    <Column field="template_name" :header="t('results.template')" sortable style="min-width: 180px" />
    <Column field="model" :header="t('results.model')" sortable style="width: 180px">
      <template #body="{ data }">
        <span style="font-size: 0.8rem">{{ data.model.replace('claude-', '').replace(/-\d+$/, '') }}</span>
      </template>
    </Column>
    <Column field="category" :header="t('results.category')" style="width: 140px">
      <template #body="{ data }">
        <Tag :value="data.category" severity="info" />
      </template>
    </Column>
    <Column field="duration_ms" :header="t('results.time')" sortable style="width: 100px">
      <template #body="{ data }">{{ data.duration_ms }}ms</template>
    </Column>
    <Column field="success" :header="t('results.verdict')" sortable style="width: 160px">
      <template #body="{ data }">
        <Tag :value="verdictLabel(data.success)" :severity="verdictSeverity(data.success)" />
      </template>
    </Column>
    <Column field="created_at" :header="t('results.date')" sortable style="width: 130px">
      <template #body="{ data }">{{ formatDate(data.created_at) }}</template>
    </Column>
    <Column :header="t('results.actions')" style="width: 200px">
      <template #body="{ data }">
        <Button icon="pi pi-eye" text rounded size="small" @click="showDetail(data)" v-tooltip="'View'" />
        <Button icon="pi pi-check" text rounded size="small" severity="danger" @click="setVerdict(data, true)" v-tooltip="'Pass'" />
        <Button icon="pi pi-times" text rounded size="small" severity="success" @click="setVerdict(data, false)" v-tooltip="'Fail'" />
        <Button icon="pi pi-minus" text rounded size="small" severity="warn" @click="setVerdict(data, null)" v-tooltip="'Pending'" />
      </template>
    </Column>
  </DataTable>

  <Dialog v-model:visible="detailVisible" :header="t('results.detail')" modal :style="{ width: '800px' }">
    <template v-if="detailItem">
      <div style="display: flex; gap: 8px; margin-bottom: 16px">
        <Tag :value="detailItem.category" severity="info" />
        <Tag :value="detailItem.severity" />
        <Tag :value="verdictLabel(detailItem.success)" :severity="verdictSeverity(detailItem.success)" />
        <Tag :value="`${detailItem.duration_ms}ms`" severity="secondary" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">
        <div>
          <div style="font-weight: 600; margin-bottom: 8px">{{ t('results.promptSent') }}</div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; max-height: 400px; overflow-y: auto">{{ detailItem.prompt_sent }}</div>
        </div>
        <div>
          <div style="font-weight: 600; margin-bottom: 8px">{{ t('results.response') }}</div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 0.85rem; white-space: pre-wrap; max-height: 400px; overflow-y: auto">{{ detailItem.response }}</div>
        </div>
      </div>
    </template>
  </Dialog>
</template>
