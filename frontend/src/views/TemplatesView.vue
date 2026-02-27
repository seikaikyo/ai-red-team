<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import { useTemplates, type TemplateForm } from '../composables/useTemplates'
import { CATEGORIES, SEVERITIES, LANGUAGES } from '../config/categories'

const toast = useToast()
const confirm = useConfirm()
const { templates, loading, fetchTemplates, createTemplate, updateTemplate, deleteTemplate } = useTemplates()

const dialogVisible = ref(false)
const editingId = ref<string | null>(null)
const saving = ref(false)

const emptyForm = (): TemplateForm => ({
  name: '',
  category: 'prompt_injection',
  severity: 'medium',
  description: '',
  prompt_template: '',
  variables: [],
  expected_behavior: '',
  tags: [],
  language: 'en',
})

const form = ref<TemplateForm>(emptyForm())
const variablesText = ref('')
const tagsText = ref('')

function openNew() {
  editingId.value = null
  form.value = emptyForm()
  variablesText.value = ''
  tagsText.value = ''
  dialogVisible.value = true
}

function openEdit(template: any) {
  editingId.value = template.id
  form.value = {
    name: template.name,
    category: template.category,
    severity: template.severity,
    description: template.description,
    prompt_template: template.prompt_template,
    variables: template.variables || [],
    expected_behavior: template.expected_behavior,
    tags: template.tags || [],
    language: template.language,
  }
  variablesText.value = (template.variables || []).join(', ')
  tagsText.value = (template.tags || []).join(', ')
  dialogVisible.value = true
}

async function save() {
  form.value.variables = variablesText.value.split(',').map(s => s.trim()).filter(Boolean)
  form.value.tags = tagsText.value.split(',').map(s => s.trim()).filter(Boolean)
  saving.value = true
  try {
    if (editingId.value) {
      await updateTemplate(editingId.value, form.value)
      toast.add({ severity: 'success', summary: 'Updated', life: 2000 })
    } else {
      await createTemplate(form.value)
      toast.add({ severity: 'success', summary: 'Created', life: 2000 })
    }
    dialogVisible.value = false
    await fetchTemplates()
  } catch (e: any) {
    toast.add({ severity: 'error', summary: 'Error', detail: e.message, life: 3000 })
  } finally {
    saving.value = false
  }
}

function confirmDelete(template: any) {
  confirm.require({
    message: `Delete "${template.name}"?`,
    header: 'Confirm',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteTemplate(template.id)
      toast.add({ severity: 'info', summary: 'Deleted', life: 2000 })
      await fetchTemplates()
    },
  })
}

function severityColor(severity: string) {
  const s = SEVERITIES.find(x => x.value === severity)
  return s?.value === 'low' ? 'success' : s?.value === 'medium' ? 'warn' : s?.value === 'high' ? 'warn' : 'danger'
}

onMounted(() => fetchTemplates())
</script>

<template>
  <div class="page-header">
    <div style="display: flex; justify-content: space-between; align-items: center">
      <div>
        <h2>Attack Templates</h2>
        <p>Manage adversarial prompt templates</p>
      </div>
      <Button label="New Template" icon="pi pi-plus" @click="openNew" />
    </div>
  </div>

  <DataTable
    :value="templates"
    :loading="loading"
    stripedRows
    paginator
    :rows="20"
    dataKey="id"
    style="background: #fff; border-radius: 12px; border: 1px solid #e2e8f0"
  >
    <Column field="name" header="Name" sortable style="min-width: 200px" />
    <Column field="category" header="Category" sortable style="width: 150px">
      <template #body="{ data }">
        <Tag :value="data.category" severity="info" />
      </template>
    </Column>
    <Column field="severity" header="Severity" sortable style="width: 120px">
      <template #body="{ data }">
        <Tag :value="data.severity" :severity="severityColor(data.severity)" />
      </template>
    </Column>
    <Column field="language" header="Lang" style="width: 80px" />
    <Column field="variables" header="Variables" style="width: 160px">
      <template #body="{ data }">
        <span v-if="data.variables?.length">{{ data.variables.join(', ') }}</span>
        <span v-else style="color: #94a3b8">--</span>
      </template>
    </Column>
    <Column header="Actions" style="width: 120px">
      <template #body="{ data }">
        <Button icon="pi pi-pencil" text rounded size="small" @click="openEdit(data)" />
        <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="confirmDelete(data)" />
      </template>
    </Column>
  </DataTable>

  <Dialog
    v-model:visible="dialogVisible"
    :header="editingId ? 'Edit Template' : 'New Template'"
    modal
    :style="{ width: '680px' }"
  >
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Name</label>
        <InputText v-model="form.name" style="width: 100%" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Category</label>
          <Select v-model="form.category" :options="CATEGORIES" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Severity</label>
          <Select v-model="form.severity" :options="[...SEVERITIES]" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Language</label>
          <Select v-model="form.language" :options="[...LANGUAGES]" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Description</label>
        <Textarea v-model="form.description" rows="2" style="width: 100%" />
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">
          Prompt Template
          <span style="font-weight: 400; color: #94a3b8">  (use &#123;&#123;var&#125;&#125; for variables)</span>
        </label>
        <Textarea v-model="form.prompt_template" rows="6" style="width: 100%; font-family: monospace" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Variables (comma-separated)</label>
          <InputText v-model="variablesText" style="width: 100%" placeholder="topic, language" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Tags (comma-separated)</label>
          <InputText v-model="tagsText" style="width: 100%" placeholder="dan, roleplay" />
        </div>
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">Expected Behavior</label>
        <Textarea v-model="form.expected_behavior" rows="2" style="width: 100%" placeholder="Model should refuse to..." />
      </div>
    </div>
    <template #footer>
      <Button label="Cancel" text @click="dialogVisible = false" />
      <Button :label="editingId ? 'Update' : 'Create'" :loading="saving" @click="save" />
    </template>
  </Dialog>
</template>
