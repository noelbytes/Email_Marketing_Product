<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import grapesjs, { type Editor } from 'grapesjs'
import 'grapesjs/dist/css/grapes.min.css'
import presetNewsletterModule from 'grapesjs-preset-newsletter'
import blocksBasicModule from 'grapesjs-blocks-basic'
import { http, ApiError } from '@/lib/httpClient'

type GrapesPlugin = (editor: Editor, opts?: Record<string, unknown>) => void

type Template = {
  id: number
  name: string
  subject?: string | null
  html: string
  css?: string | null
  project_data?: unknown | null
}

const templates = ref<Template[]>([])
const selectedId = ref<number | null>(null)
const name = ref('')
const subject = ref('')
const sendTo = ref('')
const status = ref<{ type: 'success' | 'error'; message: string } | null>(null)
const loading = ref(false)
const saving = ref(false)
const builderError = ref<string | null>(null)
const editorReady = ref(false)

const editorEl = ref<HTMLDivElement | null>(null)
let editor: Editor | null = null

const selectedTemplate = computed(() =>
  templates.value.find((tpl) => tpl.id === selectedId.value) ?? null,
)

function setStatus(type: 'success' | 'error', message: string) {
  status.value = { type, message }
  window.setTimeout(() => {
    if (status.value?.message === message) status.value = null
  }, 4500)
}

function normalizeError(err: unknown) {
  if (err instanceof ApiError) return err.message
  if (err instanceof Error) return err.message
  return 'Something went wrong'
}

async function refreshTemplates() {
  templates.value = await http<{
    data: Template[]
  }>('/templates')
    .then((resp) => resp.data)
}

async function createTemplate() {
  const templateName = `Untitled template ${new Date().toLocaleString()}`
  const created = await http<{ data: Template }>('/templates', {
    method: 'POST',
    body: JSON.stringify({
      name: templateName,
      subject: 'Welcome',
      html:
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#ffffff;border-radius:16px;padding:24px;font-family:Arial, sans-serif;">' +
        '<tr><td style="font-size:22px;font-weight:700;color:#0f172a;">Welcome to Constellation</td></tr>' +
        '<tr><td style="padding-top:12px;font-size:14px;line-height:1.6;color:#334155;">Drag blocks from the left panel to build a campaign-ready email.</td></tr>' +
        '<tr><td style="padding-top:18px;"><a href="#" style="display:inline-block;background:#7c3aed;color:#ffffff;text-decoration:none;padding:12px 16px;border-radius:999px;font-weight:600;">Primary CTA</a></td></tr>' +
        '</table>',
      css: 'body{background:#f8f4ff;}',
    }),
  })
  templates.value.unshift(created.data)
  selectedId.value = created.data.id
}

function loadIntoEditor(template: Template) {
  if (!editor) return
  editor.setComponents('')
  editor.setStyle('')
  const projectData = template.project_data
  if (projectData && typeof projectData === 'object') {
    editor.loadProjectData(projectData as Record<string, unknown>)
    return
  }
  editor.setComponents(template.html || '')
  editor.setStyle(template.css || '')
}

async function saveTemplateInternal(opts?: { silent?: boolean }): Promise<boolean> {
  if (!editor || !selectedTemplate.value) return false
  saving.value = true
  try {
    const tpl = selectedTemplate.value
    const payload = {
      name: name.value.trim() || tpl.name,
      subject: subject.value.trim() || tpl.subject,
      html: editor.getHtml(),
      css: editor.getCss(),
      project_data: editor.getProjectData(),
    }
    const updated = await http<{ data: Template }>(`/templates/${tpl.id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
    templates.value = templates.value.map((item) => (item.id === tpl.id ? updated.data : item))
    if (!opts?.silent) setStatus('success', 'Template saved')
    return true
  } catch (err) {
    if (!opts?.silent) setStatus('error', normalizeError(err))
    return false
  } finally {
    saving.value = false
  }
}

async function handleSaveClick() {
  await saveTemplateInternal()
}

async function sendTestEmail() {
  if (!selectedTemplate.value) return
  if (!sendTo.value) {
    setStatus('error', 'Enter a recipient email')
    return
  }
  try {
    const ok = await saveTemplateInternal({ silent: true })
    if (!ok) {
      setStatus('error', 'Save failed — cannot send test email')
      return
    }
    await http(`/templates/${selectedTemplate.value.id}/send-test`, {
      method: 'POST',
      body: JSON.stringify({ to: sendTo.value, subject: subject.value || undefined }),
    })
    setStatus('success', `Test email queued for ${sendTo.value}. In dev, check Mailhog (localhost:8025).`)
  } catch (err) {
    setStatus('error', normalizeError(err))
  }
}

function openBlocks() {
  try {
    editor?.Commands.run('open-blocks')
  } catch {
    // ignore
  }
}

function openStyleManager() {
  try {
    editor?.Commands.run('open-sm')
  } catch {
    // ignore
  }
}

function ensureEditor() {
  if (editor || !editorEl.value) return
  builderError.value = null
  editorReady.value = false
  try {
    const normalizePlugin = (module: unknown): GrapesPlugin => {
      if (typeof module === 'function') return module as GrapesPlugin
      if (module && typeof module === 'object' && 'default' in module) {
        const def = (module as { default?: unknown }).default
        if (typeof def === 'function') return def as GrapesPlugin
      }
      throw new Error('Invalid GrapesJS plugin module')
    }

    const presetNewsletter = normalizePlugin(presetNewsletterModule as unknown)
    const blocksBasic = normalizePlugin(blocksBasicModule as unknown)

    editor = grapesjs.init({
      container: editorEl.value,
      height: '100%',
      width: '100%',
      fromElement: false,
      storageManager: false,
      selectorManager: { componentFirst: true },
      plugins: [presetNewsletter, blocksBasic],
    })

    editorReady.value = true
    openBlocks()
  } catch (err) {
    builderError.value = normalizeError(err)
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await refreshTemplates()
    const first = templates.value[0]
    if (first) selectedId.value = first.id
  } catch (err) {
    setStatus('error', normalizeError(err))
  } finally {
    loading.value = false
  }

  try {
    await nextTick()
    ensureEditor()
  } catch (err) {
    builderError.value = normalizeError(err)
    return
  }

  if (selectedTemplate.value) {
    loadIntoEditor(selectedTemplate.value)
  }
})

onUnmounted(() => {
  editor?.destroy()
  editor = null
})

watch(
  selectedTemplate,
  (tpl) => {
    if (!tpl) return
    name.value = tpl.name
    subject.value = tpl.subject ?? ''
    ensureEditor()
    loadIntoEditor(tpl)
  },
  { immediate: true },
)
</script>

<template>
  <section class="flex flex-col gap-4">
    <header class="flex flex-col gap-3 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200 md:flex-row md:items-center md:justify-between">
      <div class="min-w-0">
        <h2 class="truncate text-lg font-semibold text-slate-900">Template Studio</h2>
        <p class="text-sm text-slate-600">
          Build, save, and send test emails. Dev inbox: <a class="font-semibold text-purple-700 underline" href="http://localhost:8025" target="_blank" rel="noreferrer">Mailhog</a>.
        </p>
      </div>
      <div class="flex flex-col gap-3 md:flex-row md:items-center">
        <input
          v-model="sendTo"
          type="email"
          placeholder="test@company.com"
          class="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400 md:w-64"
        />
        <button
          type="button"
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 disabled:opacity-50"
          :disabled="!editorReady"
          @click="openBlocks"
        >
          Blocks
        </button>
        <button
          type="button"
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 disabled:opacity-50"
          :disabled="!editorReady"
          @click="openStyleManager"
        >
          Styles
        </button>
        <button
          type="button"
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 disabled:opacity-50"
          :disabled="!selectedTemplate || saving"
          @click="handleSaveClick"
        >
          {{ saving ? 'Saving…' : 'Save' }}
        </button>
        <button
          type="button"
          class="rounded-xl bg-purple-600 px-4 py-2 text-sm font-semibold text-white hover:bg-purple-700 disabled:opacity-50"
          :disabled="!selectedTemplate"
          @click="sendTestEmail"
        >
          Send test
        </button>
      </div>
    </header>

    <p
      v-if="status"
      class="rounded-xl px-4 py-2 text-sm"
      :class="status.type === 'success' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'"
    >
      {{ status.message }}
    </p>

    <div class="grid gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
      <aside class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-slate-900">Templates</h3>
          <button
            type="button"
            class="rounded-lg bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-800"
            @click="createTemplate"
          >
            New
          </button>
        </div>
        <div v-if="loading" class="mt-4 text-sm text-slate-600">Loading…</div>
        <ul v-else class="mt-4 space-y-1">
          <li v-for="tpl in templates" :key="tpl.id">
            <button
              type="button"
              class="w-full rounded-xl px-3 py-2 text-left text-sm hover:bg-slate-50"
              :class="tpl.id === selectedId ? 'bg-purple-50 text-purple-900' : 'text-slate-800'"
              @click="selectedId = tpl.id"
            >
              <p class="truncate font-semibold">{{ tpl.name }}</p>
              <p class="truncate text-xs text-slate-500">{{ tpl.subject || 'No subject' }}</p>
            </button>
          </li>
        </ul>
        <div v-if="selectedTemplate" class="mt-6 space-y-3 border-t border-slate-200 pt-4">
          <label class="block text-xs font-semibold text-slate-700">
            Name
            <input
              v-model="name"
              class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
          </label>
          <label class="block text-xs font-semibold text-slate-700">
            Subject
            <input
              v-model="subject"
              class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
          </label>
        </div>
      </aside>

      <div class="min-w-0 rounded-2xl bg-white shadow-sm ring-1 ring-slate-200">
        <div class="relative h-[calc(100vh-18rem)] min-h-[560px]">
          <div v-if="builderError" class="m-4 rounded-xl bg-red-50 px-4 py-2 text-sm text-red-700">
            {{ builderError }}
          </div>
          <div v-else ref="editorEl" class="h-full w-full"></div>

          <div v-if="!selectedTemplate" class="absolute inset-0 grid place-items-center bg-white/70 p-6">
            <div class="max-w-sm rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <p class="text-sm font-semibold text-slate-900">No templates yet</p>
              <p class="mt-1 text-sm text-slate-600">
                Create your first template, then drag blocks into the canvas.
              </p>
              <button
                type="button"
                class="mt-4 w-full rounded-xl bg-purple-600 px-5 py-2 text-sm font-semibold text-white hover:bg-purple-700"
                @click="createTemplate"
              >
                Create first template
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
