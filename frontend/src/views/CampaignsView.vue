<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { http, ApiError } from '@/lib/httpClient'

type Template = {
  id: number
  name: string
  subject?: string | null
}

type Campaign = {
  id: number
  name: string
  status: string
  template_id: number
  subject?: string | null
  audience_type: 'all_contacts' | 'custom'
  recipients?: string[] | null
  created_at: string
}

type EmailSend = {
  id: number
  to_email: string
  status: string
  error?: string | null
  created_at: string
}

const templates = ref<Template[]>([])
const campaigns = ref<Campaign[]>([])
const selectedCampaignId = ref<number | null>(null)
const sends = ref<EmailSend[]>([])

const name = ref('New Campaign')
const templateId = ref<number | null>(null)
const subject = ref('')
const audienceType = ref<'all_contacts' | 'custom'>('all_contacts')
const recipientsText = ref('')

const status = ref<{ type: 'success' | 'error'; message: string } | null>(null)
const loading = ref(false)
const sending = ref(false)
const creating = ref(false)

const selectedCampaign = computed(
  () => campaigns.value.find((c) => c.id === selectedCampaignId.value) ?? null,
)

function normalizeError(err: unknown) {
  if (err instanceof ApiError) return err.message
  if (err instanceof Error) return err.message
  return 'Something went wrong'
}

function setStatus(type: 'success' | 'error', message: string) {
  status.value = { type, message }
  window.setTimeout(() => {
    if (status.value?.message === message) status.value = null
  }, 4500)
}

function parseRecipients(text: string): string[] {
  return text
    .split(/[\s,;\n]+/g)
    .map((s) => s.trim())
    .filter(Boolean)
}

async function refreshAll() {
  loading.value = true
  try {
    const [tplResp, campResp] = await Promise.all([
      http<{ data: Template[] }>('/templates'),
      http<{ data: Campaign[] }>('/campaigns'),
    ])
    templates.value = tplResp.data
    campaigns.value = campResp.data
    if (!selectedCampaignId.value && campaigns.value[0]) {
      selectedCampaignId.value = campaigns.value[0].id
    }
    if (!templateId.value && templates.value[0]) {
      templateId.value = templates.value[0].id
      subject.value = templates.value[0].subject ?? ''
    }
  } catch (err) {
    setStatus('error', normalizeError(err))
  } finally {
    loading.value = false
  }
}

async function createCampaign() {
  if (!templateId.value) {
    setStatus('error', 'Create a template first')
    return
  }
  creating.value = true
  try {
    const recipients = audienceType.value === 'custom' ? parseRecipients(recipientsText.value) : null
    const created = await http<{ data: Campaign }>('/campaigns', {
      method: 'POST',
      body: JSON.stringify({
        name: name.value,
        template_id: templateId.value,
        subject: subject.value || undefined,
        audience_type: audienceType.value,
        recipients: recipients?.length ? recipients : undefined,
      }),
    })
    campaigns.value = [created.data, ...campaigns.value]
    selectedCampaignId.value = created.data.id
    setStatus('success', 'Campaign created')
  } catch (err) {
    setStatus('error', normalizeError(err))
  } finally {
    creating.value = false
  }
}

async function loadSends(campaignId: number) {
  const resp = await http<{ data: EmailSend[] }>(`/campaigns/${campaignId}/sends`)
  sends.value = resp.data
}

async function sendCampaignNow() {
  if (!selectedCampaign.value) return
  sending.value = true
  try {
    await http(`/campaigns/${selectedCampaign.value.id}/send`, { method: 'POST' })
    setStatus(
      'success',
      'Campaign queued. In dev, emails are intercepted by Mailhog (localhost:8025).',
    )
    await refreshAll()
    await loadSends(selectedCampaign.value.id)
  } catch (err) {
    setStatus('error', normalizeError(err))
  } finally {
    sending.value = false
  }
}

watch(selectedCampaignId, async (id) => {
  sends.value = []
  if (!id) return
  try {
    await loadSends(id)
  } catch (err) {
    setStatus('error', normalizeError(err))
  }
})

onMounted(refreshAll)
</script>

<template>
  <section class="space-y-4">
    <header class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
      <h2 class="text-lg font-semibold text-slate-900">Campaigns</h2>
      <p class="text-sm text-slate-600">
        Create a campaign from a template and send it to an audience.
      </p>
    </header>

    <p
      v-if="status"
      class="rounded-xl px-4 py-2 text-sm"
      :class="status.type === 'success' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'"
    >
      {{ status.message }}
    </p>

    <div class="grid gap-4 lg:grid-cols-[420px_1fr]">
      <form class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200" @submit.prevent="createCampaign">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-slate-900">New campaign</h3>
          <button
            type="button"
            class="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 hover:bg-slate-50"
            :disabled="loading"
            @click="refreshAll"
          >
            Refresh
          </button>
        </div>

        <label class="mt-4 block text-xs font-semibold text-slate-700">
          Name
          <input
            v-model="name"
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          />
        </label>

        <label class="mt-3 block text-xs font-semibold text-slate-700">
          Template
          <select
            v-model="templateId"
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          >
            <option v-if="templates.length === 0" :value="null">No templates yet</option>
            <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
              {{ tpl.name }}
            </option>
          </select>
        </label>

        <label class="mt-3 block text-xs font-semibold text-slate-700">
          Subject (optional)
          <input
            v-model="subject"
            placeholder="Overrides template subject"
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          />
        </label>

        <label class="mt-3 block text-xs font-semibold text-slate-700">
          Audience
          <select
            v-model="audienceType"
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          >
            <option value="all_contacts">All contacts in workspace</option>
            <option value="custom">Custom list (emails)</option>
          </select>
        </label>

        <label v-if="audienceType === 'custom'" class="mt-3 block text-xs font-semibold text-slate-700">
          Recipients
          <textarea
            v-model="recipientsText"
            rows="4"
            placeholder="one@company.com, two@company.com"
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          />
        </label>

        <button
          type="submit"
          :disabled="creating"
          class="mt-5 w-full rounded-xl bg-purple-600 px-4 py-2 text-sm font-semibold text-white hover:bg-purple-700 disabled:opacity-50"
        >
          {{ creating ? 'Creating…' : 'Create campaign' }}
        </button>
      </form>

      <div class="space-y-4">
        <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
          <h3 class="text-sm font-semibold text-slate-900">Campaign list</h3>
          <p v-if="loading" class="mt-3 text-sm text-slate-600">Loading…</p>
          <ul v-else class="mt-3 space-y-1">
            <li v-for="camp in campaigns" :key="camp.id">
              <button
                type="button"
                class="w-full rounded-xl px-3 py-2 text-left text-sm hover:bg-slate-50"
                :class="camp.id === selectedCampaignId ? 'bg-purple-50 text-purple-900' : 'text-slate-800'"
                @click="selectedCampaignId = camp.id"
              >
                <div class="flex items-center justify-between gap-2">
                  <p class="truncate font-semibold">{{ camp.name }}</p>
                  <span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-700">
                    {{ camp.status }}
                  </span>
                </div>
                <p class="truncate text-xs text-slate-500">
                  {{ camp.audience_type === 'all_contacts' ? 'All contacts' : `${camp.recipients?.length || 0} custom recipients` }}
                </p>
              </button>
            </li>
            <li v-if="campaigns.length === 0" class="py-6 text-sm text-slate-600">
              No campaigns yet. Create your first send.
            </li>
          </ul>
        </div>

        <div v-if="selectedCampaign" class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
          <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <h3 class="text-sm font-semibold text-slate-900">Send now</h3>
              <p class="text-xs text-slate-600">Dev sends go to Mailhog (`localhost:8025`).</p>
            </div>
            <button
              type="button"
              :disabled="sending || selectedCampaign.status === 'sending' || selectedCampaign.status === 'sent'"
              class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-50"
              @click="sendCampaignNow"
            >
              {{ sending ? 'Queueing…' : 'Queue send' }}
            </button>
          </div>
        </div>

        <div v-if="selectedCampaign" class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
          <h3 class="text-sm font-semibold text-slate-900">Recent sends</h3>
          <ul class="mt-3 divide-y divide-slate-200">
            <li v-for="row in sends" :key="row.id" class="py-3">
              <div class="flex items-center justify-between gap-2">
                <p class="truncate text-sm font-semibold text-slate-900">{{ row.to_email }}</p>
                <span
                  class="rounded-full px-2 py-0.5 text-xs font-semibold"
                  :class="row.status === 'sent' ? 'bg-emerald-50 text-emerald-700' : row.status === 'failed' ? 'bg-red-50 text-red-700' : 'bg-slate-100 text-slate-700'"
                >
                  {{ row.status }}
                </span>
              </div>
              <p v-if="row.error" class="mt-1 text-xs text-red-700">{{ row.error }}</p>
            </li>
            <li v-if="sends.length === 0" class="py-6 text-sm text-slate-600">
              No sends yet.
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
