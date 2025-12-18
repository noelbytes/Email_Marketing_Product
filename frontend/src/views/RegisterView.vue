<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const { loading } = storeToRefs(auth)
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const organization = ref('')
const firstName = ref('')
const lastName = ref('')
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    await auth.register({
      email: email.value,
      password: password.value,
      organization: organization.value,
      first_name: firstName.value,
      last_name: lastName.value,
    })
    const redirect = (route.query.redirect as string) || '/app'
    router.push(redirect)
  } catch (err) {
    error.value = (err as Error).message
  }
}
</script>

<template>
  <section class="flex min-h-screen items-center justify-center bg-gradient-to-b from-white to-purple-50 px-4">
    <form
      class="w-full max-w-lg rounded-3xl bg-white p-8 shadow-2xl ring-1 ring-purple-100"
      @submit.prevent="handleSubmit"
    >
      <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Create workspace</p>
      <h1 class="mt-2 text-3xl font-bold text-slate-900">Join Constellation</h1>
      <p class="mt-1 text-sm text-slate-600">Start your mission-control workspace in seconds.</p>
      <div class="mt-6 grid gap-4 md:grid-cols-2">
        <label class="text-sm font-semibold text-slate-700">
          First name
          <input v-model="firstName" class="mt-1 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400" />
        </label>
        <label class="text-sm font-semibold text-slate-700">
          Last name
          <input v-model="lastName" class="mt-1 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400" />
        </label>
      </div>
      <label class="mt-4 block text-sm font-semibold text-slate-700">
        Work email
        <input
          v-model="email"
          type="email"
          required
          class="mt-1 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
        />
      </label>
      <label class="mt-4 block text-sm font-semibold text-slate-700">
        Password
        <input
          v-model="password"
          type="password"
          required
          class="mt-1 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
        />
      </label>
      <label class="mt-4 block text-sm font-semibold text-slate-700">
        Workspace name
        <input
          v-model="organization"
          required
          class="mt-1 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
          placeholder="orbit-collective"
        />
      </label>
      <p v-if="error" class="mt-3 rounded-xl bg-red-50 px-4 py-2 text-sm text-red-600">{{ error }}</p>
      <button
        type="submit"
        :disabled="loading"
        class="mt-6 w-full rounded-full bg-purple-600 py-3 text-sm font-semibold text-white disabled:opacity-60"
      >
        {{ loading ? 'Creating workspace…' : 'Create workspace' }}
      </button>
      <p class="mt-4 text-center text-sm text-slate-600">
        Already have an account?
        <RouterLink class="font-semibold text-purple-600" to="/login">Sign in</RouterLink>
      </p>
    </form>
  </section>
</template>
