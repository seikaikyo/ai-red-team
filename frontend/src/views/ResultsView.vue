<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
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

  <div class="filter-bar">
    <Select
      v-model="categoryFilter"
      :options="[{ value: null, label: t('results.allCategories') }, ...i18nCategories]"
      optionLabel="label"
      optionValue="value"
      :placeholder="t('results.allCategories')"
      showClear
      style="width: 200px"
      :aria-label="t('results.category')"
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
      :placeholder="t('results.allVerdicts')"
      showClear
      style="width: 200px"
      :aria-label="t('results.verdict')"
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
    class="data-table-wrap"
    :aria-label="t('results.title')"
  >
    <Column field="template_name" :header="t('results.template')" sortable style="min-width: 180px" />
    <Column field="model" :header="t('results.model')" sortable style="width: 180px">
      <template #body="{ data }">
        <span class="model-text">{{ data.model.replace('claude-', '').replace(/-\d+$/, '') }}</span>
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
        <div role="group" :aria-label="t('results.actions')">
          <Button icon="pi pi-eye" text rounded size="small" @click="showDetail(data)" v-tooltip="t('common.view')" :aria-label="t('common.view')" />
          <Button icon="pi pi-check" text rounded size="small" severity="danger" @click="setVerdict(data, true)" v-tooltip="t('results.passExploited')" :aria-label="t('results.passExploited')" />
          <Button icon="pi pi-times" text rounded size="small" severity="success" @click="setVerdict(data, false)" v-tooltip="t('results.failBlocked')" :aria-label="t('results.failBlocked')" />
          <Button icon="pi pi-minus" text rounded size="small" severity="warn" @click="setVerdict(data, null)" v-tooltip="t('results.pending')" :aria-label="t('results.pending')" />
        </div>
      </template>
    </Column>
  </DataTable>

  <Dialog v-model:visible="detailVisible" :header="t('results.detail')" modal :style="{ width: '800px', maxWidth: '95vw' }">
    <template v-if="detailItem">
      <div class="detail-tags">
        <Tag :value="detailItem.category" severity="info" />
        <Tag :value="detailItem.severity" />
        <Tag :value="verdictLabel(detailItem.success)" :severity="verdictSeverity(detailItem.success)" />
        <Tag :value="`${detailItem.duration_ms}ms`" severity="secondary" />
      </div>
      <div class="detail-grid">
        <div>
          <div class="detail-section-title">{{ t('results.promptSent') }}</div>
          <div class="detail-content">{{ detailItem.prompt_sent }}</div>
        </div>
        <div>
          <div class="detail-section-title">{{ t('results.response') }}</div>
          <div class="detail-content-response">{{ detailItem.response }}</div>
        </div>
      </div>
    </template>
  </Dialog>
</template>
