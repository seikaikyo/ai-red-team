<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import ToggleSwitch from 'primevue/toggleswitch'
import Message from 'primevue/message'
import { useTemplates, type AttackTemplate } from '../composables/useTemplates'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
import { MODELS, CATEGORIES, LANGUAGES, CUSTOM_PROVIDER_PRESETS, type ProviderPreset } from '../config/categories'
import { useI18n } from '../composables/useI18n'

const toast = useToast()
const { t, locale } = useI18n()
const { templates, fetchTemplates } = useTemplates()
const { running, runTest } = useTestRunner()

const selectedTemplate = ref<AttackTemplate | null>(null)
const selectedModel = ref(MODELS[0]?.value ?? 'claude-sonnet-5')
const maxTokens = ref(1024)
const temperature = ref(1.0)
const variables = ref<Record<string, string>>({})
const lastResult = ref<TestRun | null>(null)
const isDemo = import.meta.env.VITE_DEMO_MODE === '1'
const categoryFilter = ref<string | null>(null)
const langFilter = ref<string | null>(null)

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

const langOptions = computed(() => [
  { value: null, label: t('runner.allCategories') },
  ...LANGUAGES.map(l => ({ value: l.value, label: l.label })),
])

const filteredTemplates = computed(() => {
  let list = templates.value
  if (categoryFilter.value) {
    list = list.filter(t => t.category === categoryFilter.value)
  }
  return list
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

function loadTemplates() {
  const lang = langFilter.value ?? locale.value
  fetchTemplates({ language: lang })
}

watch([locale, langFilter], () => {
  selectedTemplate.value = null
  loadTemplates()
})
onMounted(() => loadTemplates())
</script>

<template>
  <Message v-if="isDemo" severity="info" :closable="false">{{ t('runner.demoBanner') }}</Message>

  <div class="page-header">
    <h2>{{ t('runner.title') }}</h2>
    <p>{{ t('runner.subtitle') }}</p>
  </div>

  <div class="grid-2">
    <!-- Left: Config -->
    <div class="flex-col gap-16">
      <div class="stat-card">
        <div class="card-title">{{ t('runner.config') }}</div>
        <div class="flex-col gap-12">
          <div class="grid-2" style="gap: 8px">
            <div>
              <label class="form-label" for="runner-category">{{ t('runner.categoryFilter') }}</label>
              <Select
                id="runner-category"
                v-model="categoryFilter"
                :options="[{ value: null, label: t('runner.allCategories') }, ...i18nCategories]"
                optionLabel="label"
                optionValue="value"
                style="width: 100%"
                showClear
              />
            </div>
            <div>
              <label class="form-label" for="runner-lang">{{ t('templates.lang') }}</label>
              <Select
                id="runner-lang"
                v-model="langFilter"
                :options="langOptions"
                optionLabel="label"
                optionValue="value"
                style="width: 100%"
              />
            </div>
          </div>
          <div>
            <label class="form-label" for="runner-template">{{ t('runner.template') }}</label>
            <Select
              id="runner-template"
              v-model="selectedTemplate"
              :options="filteredTemplates"
              optionLabel="name"
              :placeholder="t('runner.selectTemplate')"
              style="width: 100%"
              filter
            />
          </div>
          <div>
            <label class="form-label" for="runner-model">{{ t('runner.targetModel') }}</label>
            <Select v-if="!useCustomModel" id="runner-model" v-model="selectedModel" :options="[...MODELS]" optionLabel="label" optionValue="value" style="width: 100%" />
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px">
              <ToggleSwitch v-model="useCustomModel" inputId="custom-toggle" />
              <label for="custom-toggle" style="font-size: 0.8rem; color: var(--color-text-secondary); cursor: pointer">{{ t('runner.useCustomModel') }}</label>
            </div>
          </div>
          <div v-if="useCustomModel" class="flex-col gap-12 custom-provider-box">
            <div>
              <label class="form-label">{{ t('runner.provider') }}</label>
              <SelectButton v-model="customProvider" :options="providerOptions" optionLabel="label" optionValue="value" :allowEmpty="false" style="width: 100%" />
            </div>
            <div>
              <label class="form-label" for="runner-baseurl">{{ t('runner.baseUrl') }}</label>
              <InputText id="runner-baseurl" v-model="customBaseUrl" style="width: 100%" placeholder="http://localhost:11434/v1" />
            </div>
            <div>
              <label class="form-label" for="runner-modelname">{{ t('runner.modelName') }}</label>
              <InputText id="runner-modelname" v-model="customModelName" style="width: 100%" :placeholder="t('runner.modelNamePlaceholder')" />
            </div>
          </div>
          <div class="grid-2" style="gap: 8px">
            <div>
              <label class="form-label" for="runner-tokens">{{ t('runner.maxTokens') }}</label>
              <InputNumber id="runner-tokens" v-model="maxTokens" :min="1" :max="4096" style="width: 100%" />
            </div>
            <div>
              <label class="form-label" for="runner-temp">{{ t('runner.temperature') }}</label>
              <InputNumber id="runner-temp" v-model="temperature" :min="0" :max="1" :step="0.1" :minFractionDigits="1" style="width: 100%" />
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedTemplate && selectedTemplate.variables?.length" class="stat-card">
        <div class="card-title">{{ t('runner.variables') }}</div>
        <div class="flex-col gap-8">
          <div v-for="v in selectedTemplate.variables" :key="v">
            <label class="form-label" :for="`var-${v}`" v-text="'{{' + v + '}}'"></label>
            <InputText :id="`var-${v}`" v-model="variables[v]" style="width: 100%" :placeholder="t('runner.enterVar', { var: v })" />
          </div>
        </div>
      </div>

      <Button
        :label="t('runner.executeBtn')"
        icon="pi pi-play"
        :loading="running"
        :disabled="isDemo || !selectedTemplate"
        @click="execute"
        style="width: 100%"
        severity="danger"
        :aria-label="t('runner.executeBtn')"
      />
    </div>

    <!-- Right: Prompt + Response -->
    <div class="flex-col gap-16">
      <div class="stat-card" style="flex: 1">
        <div class="card-title" style="margin-bottom: 8px">{{ t('runner.promptPreview') }}</div>
        <div v-if="selectedTemplate" class="code-block">{{ resolvedPrompt }}</div>
        <div v-else class="empty-state">{{ t('runner.selectToPreview') }}</div>
      </div>

      <div class="stat-card" style="flex: 1">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <span class="card-title" style="margin-bottom: 0">{{ t('runner.response') }}</span>
          <Tag v-if="lastResult" :value="`${lastResult.duration_ms}ms`" severity="info" />
        </div>
        <div v-if="lastResult" class="code-block-lg">{{ lastResult.response }}</div>
        <div v-else class="empty-state">{{ t('runner.runToSee') }}</div>
      </div>
    </div>
  </div>
</template>
