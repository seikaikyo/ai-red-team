<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
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
import { useI18n } from '../composables/useI18n'

const toast = useToast()
const confirm = useConfirm()
const { t, locale } = useI18n()
const { templates, loading, fetchTemplates, createTemplate, updateTemplate, deleteTemplate } = useTemplates()

const langFilter = ref<string | null>(null)
const dialogVisible = ref(false)
const editingId = ref<string | null>(null)
const saving = ref(false)

const langOptions = computed(() => [
  { value: null, label: t('runner.allCategories') },
  ...LANGUAGES.map(l => ({ value: l.value, label: l.label })),
])

const emptyForm = (): TemplateForm => ({
  name: '',
  category: 'prompt_injection',
  severity: 'medium',
  description: '',
  prompt_template: '',
  variables: [],
  expected_behavior: '',
  tags: [],
  language: locale.value,
})

const form = ref<TemplateForm>(emptyForm())
const variablesText = ref('')
const tagsText = ref('')

const i18nCategories = computed(() =>
  CATEGORIES.map(c => ({ ...c, label: t(c.labelKey) }))
)
const i18nSeverities = computed(() =>
  SEVERITIES.map(s => ({ ...s, label: t(s.labelKey) }))
)

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
      toast.add({ severity: 'success', summary: t('common.updated'), life: 2000 })
    } else {
      await createTemplate(form.value)
      toast.add({ severity: 'success', summary: t('common.created'), life: 2000 })
    }
    dialogVisible.value = false
    await loadTemplates()
  } catch (e: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: e.message, life: 3000 })
  } finally {
    saving.value = false
  }
}

function confirmDelete(template: any) {
  confirm.require({
    message: t('common.deleteConfirm', { name: template.name }),
    header: t('common.confirm'),
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteTemplate(template.id)
      toast.add({ severity: 'info', summary: t('common.deleted'), life: 2000 })
      await loadTemplates()
    },
  })
}

function severityColor(severity: string) {
  const s = SEVERITIES.find(x => x.value === severity)
  return s?.value === 'low' ? 'success' : s?.value === 'medium' ? 'warn' : s?.value === 'high' ? 'warn' : 'danger'
}

function loadTemplates() {
  const lang = langFilter.value ?? locale.value
  fetchTemplates({ language: lang })
}

watch([locale, langFilter], () => loadTemplates())
onMounted(() => loadTemplates())
</script>

<template>
  <div class="page-header">
    <div style="display: flex; justify-content: space-between; align-items: center">
      <div>
        <h2>{{ t('templates.title') }}</h2>
        <p>{{ t('templates.subtitle') }}</p>
      </div>
      <div style="display: flex; align-items: center; gap: 8px">
        <Select
          v-model="langFilter"
          :options="langOptions"
          optionLabel="label"
          optionValue="value"
          style="width: 160px"
          :placeholder="t('templates.lang')"
        />
        <Button :label="t('templates.newBtn')" icon="pi pi-plus" @click="openNew" />
      </div>
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
    <Column field="name" :header="t('templates.name')" sortable style="min-width: 200px" />
    <Column field="category" :header="t('templates.category')" sortable style="width: 150px">
      <template #body="{ data }">
        <Tag :value="data.category" severity="info" />
      </template>
    </Column>
    <Column field="severity" :header="t('templates.severity')" sortable style="width: 120px">
      <template #body="{ data }">
        <Tag :value="data.severity" :severity="severityColor(data.severity)" />
      </template>
    </Column>
    <Column field="language" :header="t('templates.lang')" style="width: 80px" />
    <Column field="variables" :header="t('templates.variables')" style="width: 160px">
      <template #body="{ data }">
        <span v-if="data.variables?.length">{{ data.variables.join(', ') }}</span>
        <span v-else style="color: #94a3b8">--</span>
      </template>
    </Column>
    <Column :header="t('templates.actions')" style="width: 120px">
      <template #body="{ data }">
        <Button icon="pi pi-pencil" text rounded size="small" @click="openEdit(data)" />
        <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="confirmDelete(data)" />
      </template>
    </Column>
  </DataTable>

  <Dialog
    v-model:visible="dialogVisible"
    :header="editingId ? t('templates.editDialog') : t('templates.newDialog')"
    modal
    :style="{ width: '680px' }"
  >
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.name') }}</label>
        <InputText v-model="form.name" style="width: 100%" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.category') }}</label>
          <Select v-model="form.category" :options="i18nCategories" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.severity') }}</label>
          <Select v-model="form.severity" :options="i18nSeverities" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.language') }}</label>
          <Select v-model="form.language" :options="[...LANGUAGES]" optionLabel="label" optionValue="value" style="width: 100%" />
        </div>
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.description') }}</label>
        <Textarea v-model="form.description" rows="2" style="width: 100%" />
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">
          {{ t('templates.promptTemplate') }}
          <span style="font-weight: 400; color: #94a3b8">  {{ t('templates.promptHint') }}</span>
        </label>
        <Textarea v-model="form.prompt_template" rows="6" style="width: 100%; font-family: monospace" />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.variablesComma') }}</label>
          <InputText v-model="variablesText" style="width: 100%" placeholder="topic, language" />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.tagsComma') }}</label>
          <InputText v-model="tagsText" style="width: 100%" placeholder="dan, roleplay" />
        </div>
      </div>
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 4px">{{ t('templates.expectedBehavior') }}</label>
        <Textarea v-model="form.expected_behavior" rows="2" style="width: 100%" :placeholder="t('templates.expectedPlaceholder')" />
      </div>
    </div>
    <template #footer>
      <Button :label="t('common.cancel')" text @click="dialogVisible = false" />
      <Button :label="editingId ? t('common.update') : t('common.create')" :loading="saving" @click="save" />
    </template>
  </Dialog>
</template>
