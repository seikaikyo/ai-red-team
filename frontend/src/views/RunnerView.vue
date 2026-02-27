<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import ToggleSwitch from 'primevue/toggleswitch'
import { useTemplates, type AttackTemplate } from '../composables/useTemplates'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
import { MODELS, CATEGORIES, CUSTOM_PROVIDER_PRESETS, type ProviderPreset } from '../config/categories'
import { useI18n } from '../composables/useI18n'

const toast = useToast()
const { t } = useI18n()
const { templates, fetchTemplates } = useTemplates()
const { running, runTest } = useTestRunner()

const selectedTemplate = ref<AttackTemplate | null>(null)
const selectedModel = ref(MODELS[0].value)
const maxTokens = ref(1024)
const temperature = ref(1.0)
const variables = ref<Record<string, string>>({})
const lastResult = ref<TestRun | null>(null)
const categoryFilter = ref<string | null>(null)

// 自訂模型
const useCustomModel = ref(false)
const customProvider = ref<ProviderPreset>('ollama')
const customBaseUrl = ref<string>(CUSTOM_PROVIDER_PRESETS[0].defaultUrl)
const customModelName = ref('')

const providerOptions = CUSTOM_PROVIDER_PRESETS.map(p => ({ label: p.label, value: p.value }))

watch(customProvider, (val) => {
  const preset = CUSTOM_PROVIDER_PRESETS.find(p => p.value === val)
  if (preset && preset.defaultUrl) {
    customBaseUrl.value = preset.defaultUrl
  }
})

const i18nCategories = computed(() =>
  CATEGORIES.map(c => ({ ...c, label: t(c.labelKey) }))
)

const filteredTemplates = computed(() => {
  if (!categoryFilter.value) return templates.value
  return templates.value.filter(t => t.category === categoryFilter.value)
})

watch(selectedTemplate, (t) => {
  if (!t) return
  variables.value = {}
  for (const v of t.variables || []) {
    variables.value[v] = ''
  }
})

const resolvedPrompt = computed(() => {
  if (!selectedTemplate.value) return ''
  let prompt = selectedTemplate.value.prompt_template
  for (const [key, val] of Object.entries(variables.value)) {
    prompt = prompt.replaceAll(`{{${key}}}`, val || `{{${key}}}`)
  }
  return prompt
})

const effectiveModel = computed(() =>
  useCustomModel.value ? customModelName.value : selectedModel.value
)

const effectiveBaseUrl = computed(() =>
  useCustomModel.value ? customBaseUrl.value : null
)

async function execute() {
  if (!selectedTemplate.value) return
  if (useCustomModel.value && !customModelName.value.trim()) {
    toast.add({ severity: 'warn', summary: t('common.error'), detail: t('runner.modelNameRequired'), life: 3000 })
    return
  }
  try {
    lastResult.value = await runTest({
      template_id: selectedTemplate.value.id,
      model: effectiveModel.value,
      variables: variables.value,
      max_tokens: maxTokens.value,
      temperature: temperature.value,
      base_url: effectiveBaseUrl.value,
    })
    toast.add({ severity: 'success', summary: t('runner.testCompleted'), detail: `${lastResult.value.duration_ms}ms`, life: 3000 })
  } catch (e: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: e.message, life: 5000 })
  }
}

onMounted(() => fetchTemplates())
</script>

<template>
  <div class="page-header">
    <h2>{{ t('runner.title') }}</h2>
    <p>{{ t('runner.subtitle') }}</p>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
    <!-- Left: Config -->
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="stat-card">
        <div style="font-weight: 600; margin-bottom: 12px">{{ t('runner.config') }}</div>
        <div style="display: flex; flex-direction: column; gap: 12px">
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.categoryFilter') }}</label>
            <Select
              v-model="categoryFilter"
              :options="[{ value: null, label: t('runner.allCategories') }, ...i18nCategories]"
              optionLabel="label"
              optionValue="value"
              style="width: 100%"
              showClear
            />
          </div>
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.template') }}</label>
            <Select
              v-model="selectedTemplate"
              :options="filteredTemplates"
              optionLabel="name"
              :placeholder="t('runner.selectTemplate')"
              style="width: 100%"
              filter
            />
          </div>
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.targetModel') }}</label>
            <Select v-if="!useCustomModel" v-model="selectedModel" :options="[...MODELS]" optionLabel="label" optionValue="value" style="width: 100%" />
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px">
              <ToggleSwitch v-model="useCustomModel" />
              <span style="font-size: 0.8rem; color: #64748b">{{ t('runner.useCustomModel') }}</span>
            </div>
          </div>
          <div v-if="useCustomModel" style="display: flex; flex-direction: column; gap: 10px; padding: 12px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0">
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.provider') }}</label>
              <SelectButton v-model="customProvider" :options="providerOptions" optionLabel="label" optionValue="value" :allowEmpty="false" style="width: 100%" />
            </div>
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.baseUrl') }}</label>
              <InputText v-model="customBaseUrl" style="width: 100%" placeholder="http://localhost:11434/v1" />
            </div>
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.modelName') }}</label>
              <InputText v-model="customModelName" style="width: 100%" :placeholder="t('runner.modelNamePlaceholder')" />
            </div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.maxTokens') }}</label>
              <InputNumber v-model="maxTokens" :min="1" :max="4096" style="width: 100%" />
            </div>
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">{{ t('runner.temperature') }}</label>
              <InputNumber v-model="temperature" :min="0" :max="1" :step="0.1" :minFractionDigits="1" style="width: 100%" />
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedTemplate && selectedTemplate.variables?.length" class="stat-card">
        <div style="font-weight: 600; margin-bottom: 12px">{{ t('runner.variables') }}</div>
        <div style="display: flex; flex-direction: column; gap: 8px">
          <div v-for="v in selectedTemplate.variables" :key="v">
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px" v-text="'{{' + v + '}}'"></label>
            <InputText v-model="variables[v]" style="width: 100%" :placeholder="t('runner.enterVar', { var: v })" />
          </div>
        </div>
      </div>

      <Button
        :label="t('runner.executeBtn')"
        icon="pi pi-play"
        :loading="running"
        :disabled="!selectedTemplate"
        @click="execute"
        style="width: 100%"
        severity="danger"
      />
    </div>

    <!-- Right: Prompt + Response -->
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="stat-card" style="flex: 1">
        <div style="font-weight: 600; margin-bottom: 8px">{{ t('runner.promptPreview') }}</div>
        <div v-if="selectedTemplate" style="background: #f8fafc; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; max-height: 280px; overflow-y: auto; border: 1px solid #e2e8f0">{{ resolvedPrompt }}</div>
        <div v-else style="color: #94a3b8; padding: 24px; text-align: center">{{ t('runner.selectToPreview') }}</div>
      </div>

      <div class="stat-card" style="flex: 1">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <span style="font-weight: 600">{{ t('runner.response') }}</span>
          <Tag v-if="lastResult" :value="`${lastResult.duration_ms}ms`" severity="info" />
        </div>
        <div v-if="lastResult" style="background: #f8fafc; border-radius: 8px; padding: 12px; font-size: 0.85rem; white-space: pre-wrap; max-height: 320px; overflow-y: auto; border: 1px solid #e2e8f0">{{ lastResult.response }}</div>
        <div v-else style="color: #94a3b8; padding: 24px; text-align: center">{{ t('runner.runToSee') }}</div>
      </div>
    </div>
  </div>
</template>
