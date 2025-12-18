<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { http, ApiError } from '@/lib/httpClient'
import { useAuthStore } from '@/stores/auth'

type Contact = {
  id: number
  email: string
  first_name?: string | null
  last_name?: string | null
  organization_id: number
  created_at: string
}

const auth = useAuthStore()
const orgId = computed(() => auth.user?.organization_id ?? null)

const contacts = ref<Contact[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const email = ref('')
const firstName = ref('')
const lastName = ref('')
const creating = ref(false)

function normalizeError(err: unknown) {
  if (err instanceof ApiError) return err.message
  if (err instanceof Error) return err.message
  return 'Something went wrong'
}

async function loadContacts() {
  if (!orgId.value) return
  loading.value = true
  error.value = null
  try {
    const resp = await http<{ data: Contact[] }>(`/organizations/${orgId.value}/contacts`)
    contacts.value = resp.data
  } catch (err) {
    error.value = normalizeError(err)
  } finally {
    loading.value = false
  }
}

async function createContact() {
  if (!orgId.value) return
  creating.value = true
  error.value = null
  try {
    const resp = await http<{ data: Contact }>(`/organizations/${orgId.value}/contacts`, {
      method: 'POST',
      body: JSON.stringify({
        email: email.value,
        first_name: firstName.value || undefined,
        last_name: lastName.value || undefined,
      }),
    })
    contacts.value = [resp.data, ...contacts.value]
    email.value = ''
    firstName.value = ''
    lastName.value = ''
  } catch (err) {
    error.value = normalizeError(err)
  } finally {
    creating.value = false
  }
}

onMounted(loadContacts)
</script>

<template>
  <section class="space-y-4">
    <header class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
      <h2 class="text-lg font-semibold text-slate-900">Contacts</h2>
      <p class="text-sm text-slate-600">Build audiences by collecting verified recipients.</p>
    </header>

    <div v-if="error" class="rounded-xl bg-red-50 px-4 py-2 text-sm text-red-700">{{ error }}</div>

    <div class="grid gap-4 lg:grid-cols-[420px_1fr]">
      <form
        class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200"
        @submit.prevent="createContact"
      >
        <h3 class="text-sm font-semibold text-slate-900">Add contact</h3>
        <label class="mt-4 block text-xs font-semibold text-slate-700">
          Email
          <input
            v-model="email"
            type="email"
            required
            class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
          />
        </label>
        <div class="mt-3 grid gap-3 md:grid-cols-2">
          <label class="block text-xs font-semibold text-slate-700">
            First name
            <input
              v-model="firstName"
              class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
          </label>
          <label class="block text-xs font-semibold text-slate-700">
            Last name
            <input
              v-model="lastName"
              class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
          </label>
        </div>
        <button
          type="submit"
          :disabled="creating"
          class="mt-5 w-full rounded-xl bg-purple-600 px-4 py-2 text-sm font-semibold text-white hover:bg-purple-700 disabled:opacity-50"
        >
          {{ creating ? 'Saving…' : 'Add contact' }}
        </button>
      </form>

      <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-slate-900">Workspace contacts</h3>
          <button
            type="button"
            class="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 hover:bg-slate-50"
            :disabled="loading"
            @click="loadContacts"
          >
            Refresh
          </button>
        </div>
        <p v-if="loading" class="mt-4 text-sm text-slate-600">Loading…</p>
        <ul v-else class="mt-4 divide-y divide-slate-200">
          <li v-for="contact in contacts" :key="contact.id" class="py-3">
            <p class="text-sm font-semibold text-slate-900">{{ contact.email }}</p>
            <p class="text-xs text-slate-600">
              {{ [contact.first_name, contact.last_name].filter(Boolean).join(' ') || '—' }}
            </p>
          </li>
          <li v-if="contacts.length === 0" class="py-6 text-sm text-slate-600">
            No contacts yet. Add your first recipient.
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

