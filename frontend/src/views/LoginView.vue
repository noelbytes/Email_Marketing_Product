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
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    await auth.login({
      email: email.value,
      password: password.value,
      organization: organization.value,
    })
    const redirect = (route.query.redirect as string) || '/app'
    router.push(redirect)
  } catch (err) {
    error.value = (err as Error).message
  } finally {
  }
}
</script>

<template>
  <section class="flex min-h-screen items-center justify-center bg-gradient-to-b from-white to-purple-50 px-4">
    <form
      class="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl ring-1 ring-purple-100"
      @submit.prevent="handleSubmit"
    >
      <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Mission Control</p>
      <h1 class="mt-2 text-3xl font-bold text-slate-900">Welcome back</h1>
      <p class="text-sm text-slate-600">Sign in to orchestrate your journeys.</p>
      <label class="mt-6 block text-sm font-semibold text-slate-700">
        Email
        <input
          v-model="email"
          name="email"
          type="email"
          required
          placeholder="you@brand.com"
          class="mt-2 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
        />
      </label>
      <label class="mt-4 block text-sm font-semibold text-slate-700">
        Password
        <input
          v-model="password"
          name="password"
          type="password"
          required
          placeholder="••••••••"
          class="mt-2 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
        />
      </label>
      <label class="mt-4 block text-sm font-semibold text-slate-700">
        Workspace
        <input
          v-model="organization"
          name="organization"
          type="text"
          placeholder="orbit-collective"
          class="mt-2 w-full rounded-2xl border border-purple-100 px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
        />
      </label>
      <p v-if="error" class="mt-3 rounded-xl bg-red-50 px-4 py-2 text-sm text-red-600">{{ error }}</p>
      <button
        type="submit"
        :disabled="loading"
        class="mt-6 w-full rounded-full bg-purple-600 py-3 text-sm font-semibold text-white disabled:opacity-60"
      >
        {{ loading ? 'Signing in…' : 'Take me to Mission Control' }}
      </button>
      <p class="mt-4 text-center text-sm text-slate-600">
        Need a workspace?
        <RouterLink class="font-semibold text-purple-600" to="/register">Create one</RouterLink>
      </p>
    </form>
  </section>
</template>
