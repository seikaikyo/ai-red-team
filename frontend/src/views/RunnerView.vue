<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import { useTemplates, type AttackTemplate } from '../composables/useTemplates'
import { useTestRunner, type TestRun } from '../composables/useTestRunner'
import { MODELS, CATEGORIES } from '../config/categories'

const toast = useToast()
const { templates, fetchTemplates } = useTemplates()
const { running, runTest } = useTestRunner()

const selectedTemplate = ref<AttackTemplate | null>(null)
const selectedModel = ref(MODELS[0].value)
const maxTokens = ref(1024)
const temperature = ref(1.0)
const variables = ref<Record<string, string>>({})
const lastResult = ref<TestRun | null>(null)
const categoryFilter = ref<string | null>(null)

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

async function execute() {
  if (!selectedTemplate.value) return
  try {
    lastResult.value = await runTest({
      template_id: selectedTemplate.value.id,
      model: selectedModel.value,
      variables: variables.value,
      max_tokens: maxTokens.value,
      temperature: temperature.value,
    })
    toast.add({ severity: 'success', summary: 'Test completed', detail: `${lastResult.value.duration_ms}ms`, life: 3000 })
  } catch (e: any) {
    toast.add({ severity: 'error', summary: 'Error', detail: e.message, life: 5000 })
  }
}

onMounted(() => fetchTemplates())
</script>

<template>
  <div class="page-header">
    <h2>Test Runner</h2>
    <p>Execute adversarial prompts against target models</p>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
    <!-- Left: Config -->
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="stat-card">
        <div style="font-weight: 600; margin-bottom: 12px">Configuration</div>
        <div style="display: flex; flex-direction: column; gap: 12px">
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">Category Filter</label>
            <Select
              v-model="categoryFilter"
              :options="[{ value: null, label: 'All Categories' }, ...CATEGORIES]"
              optionLabel="label"
              optionValue="value"
              style="width: 100%"
              showClear
            />
          </div>
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">Template</label>
            <Select
              v-model="selectedTemplate"
              :options="filteredTemplates"
              optionLabel="name"
              placeholder="Select a template"
              style="width: 100%"
              filter
            />
          </div>
          <div>
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">Target Model</label>
            <Select v-model="selectedModel" :options="[...MODELS]" optionLabel="label" optionValue="value" style="width: 100%" />
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">Max Tokens</label>
              <InputNumber v-model="maxTokens" :min="1" :max="4096" style="width: 100%" />
            </div>
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px">Temperature</label>
              <InputNumber v-model="temperature" :min="0" :max="1" :step="0.1" :minFractionDigits="1" style="width: 100%" />
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedTemplate && selectedTemplate.variables?.length" class="stat-card">
        <div style="font-weight: 600; margin-bottom: 12px">Variables</div>
        <div style="display: flex; flex-direction: column; gap: 8px">
          <div v-for="v in selectedTemplate.variables" :key="v">
            <label style="display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px" v-text="'{{' + v + '}}'"></label>
            <InputText v-model="variables[v]" style="width: 100%" :placeholder="`Enter ${v}`" />
          </div>
        </div>
      </div>

      <Button
        label="Execute Test"
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
        <div style="font-weight: 600; margin-bottom: 8px">Prompt Preview</div>
        <div v-if="selectedTemplate" style="background: #f8fafc; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; max-height: 280px; overflow-y: auto; border: 1px solid #e2e8f0">{{ resolvedPrompt }}</div>
        <div v-else style="color: #94a3b8; padding: 24px; text-align: center">Select a template to preview</div>
      </div>

      <div class="stat-card" style="flex: 1">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <span style="font-weight: 600">Response</span>
          <Tag v-if="lastResult" :value="`${lastResult.duration_ms}ms`" severity="info" />
        </div>
        <div v-if="lastResult" style="background: #f8fafc; border-radius: 8px; padding: 12px; font-size: 0.85rem; white-space: pre-wrap; max-height: 320px; overflow-y: auto; border: 1px solid #e2e8f0">{{ lastResult.response }}</div>
        <div v-else style="color: #94a3b8; padding: 24px; text-align: center">Run a test to see the response</div>
      </div>
    </div>
  </div>
</template>
