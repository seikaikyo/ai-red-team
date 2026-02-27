<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

const toast = useToast()
const { results, loading, fetchResults, updateVerdict } = useTestRunner()

const detailVisible = ref(false)
const detailItem = ref<TestRun | null>(null)
const categoryFilter = ref<string | null>(null)
const successFilter = ref<string | null>(null)

function showDetail(item: TestRun) {
  detailItem.value = item
  detailVisible.value = true
}

async function setVerdict(item: TestRun, success: boolean | null) {
  try {
    await updateVerdict(item.id, success)
    item.success = success
    toast.add({ severity: 'success', summary: 'Verdict updated', life: 2000 })
  } catch (e: any) {
    toast.add({ severity: 'error', summary: 'Error', detail: e.message })
  }
}

function verdictSeverity(s: boolean | null) {
  if (s === true) return 'danger'
  if (s === false) return 'success'
  return 'warn'
}

function verdictLabel(s: boolean | null) {
  if (s === true) return 'Pass (Exploited)'
  if (s === false) return 'Fail (Blocked)'
  return 'Pending'
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
    <h2>Test Results</h2>
    <p>Review and judge test outcomes</p>
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
      @change="reload"
    />
    <Select
      v-model="successFilter"
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
    <Column field="template_name" header="Template" sortable style="min-width: 180px" />
    <Column field="model" header="Model" sortable style="width: 180px">
      <template #body="{ data }">
        <span style="font-size: 0.8rem">{{ data.model.replace('claude-', '').replace(/-\d+$/, '') }}</span>
      </template>
    </Column>
    <Column field="category" header="Category" style="width: 140px">
      <template #body="{ data }">
        <Tag :value="data.category" severity="info" />
      </template>
    </Column>
    <Column field="duration_ms" header="Time" sortable style="width: 100px">
      <template #body="{ data }">{{ data.duration_ms }}ms</template>
    </Column>
    <Column field="success" header="Verdict" sortable style="width: 160px">
      <template #body="{ data }">
        <Tag :value="verdictLabel(data.success)" :severity="verdictSeverity(data.success)" />
      </template>
    </Column>
    <Column field="created_at" header="Date" sortable style="width: 130px">
      <template #body="{ data }">{{ formatDate(data.created_at) }}</template>
    </Column>
    <Column header="Actions" style="width: 200px">
      <template #body="{ data }">
        <Button icon="pi pi-eye" text rounded size="small" @click="showDetail(data)" v-tooltip="'View'" />
        <Button icon="pi pi-check" text rounded size="small" severity="danger" @click="setVerdict(data, true)" v-tooltip="'Mark Pass'" />
        <Button icon="pi pi-times" text rounded size="small" severity="success" @click="setVerdict(data, false)" v-tooltip="'Mark Fail'" />
        <Button icon="pi pi-minus" text rounded size="small" severity="warn" @click="setVerdict(data, null)" v-tooltip="'Pending'" />
      </template>
    </Column>
  </DataTable>

  <Dialog v-model:visible="detailVisible" header="Test Detail" modal :style="{ width: '800px' }">
    <template v-if="detailItem">
      <div style="display: flex; gap: 8px; margin-bottom: 16px">
        <Tag :value="detailItem.category" severity="info" />
        <Tag :value="detailItem.severity" />
        <Tag :value="verdictLabel(detailItem.success)" :severity="verdictSeverity(detailItem.success)" />
        <Tag :value="`${detailItem.duration_ms}ms`" severity="secondary" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">
        <div>
          <div style="font-weight: 600; margin-bottom: 8px">Prompt Sent</div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; max-height: 400px; overflow-y: auto">{{ detailItem.prompt_sent }}</div>
        </div>
        <div>
          <div style="font-weight: 600; margin-bottom: 8px">Response</div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 0.85rem; white-space: pre-wrap; max-height: 400px; overflow-y: auto">{{ detailItem.response }}</div>
        </div>
      </div>
    </template>
  </Dialog>
</template>
