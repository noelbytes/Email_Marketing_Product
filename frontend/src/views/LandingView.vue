<script setup lang="ts">
const stats = [
  { label: 'Avg ROI', value: '8.4x' },
  { label: 'Journeys automated', value: '12,400+' },
  { label: 'Deliverability', value: '99.3%' },
]

const differentiators = [
  {
    title: 'Mission Control',
    description: 'Unified dashboard for journeys, insights, and compliance readiness.',
  },
  {
    title: 'AI Template Studio',
    description: 'Drag-and-drop content blocks with AI copy, localization, and approvals.',
  },
  {
    title: 'Enterprise IAM',
    description: 'SSO, SCIM, RBAC, and audit trails built natively for regulated teams.',
  },
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-purple-50">
    <nav class="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
      <div class="flex items-center gap-2">
        <span class="rounded-xl bg-purple-600 px-3 py-1 text-sm font-semibold text-white">β</span>
        <div>
          <p class="font-semibold text-slate-900">Constellation</p>
          <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Marketing Studio</p>
        </div>
      </div>
      <div class="hidden items-center gap-4 md:flex">
        <RouterLink to="/login" class="text-sm font-semibold text-slate-700">Login</RouterLink>
        <RouterLink
          to="/register"
          class="rounded-full bg-purple-600 px-4 py-2 text-sm font-semibold text-white"
        >
          Get Started
        </RouterLink>
      </div>
    </nav>

    <header class="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-6 py-10 md:grid-cols-2">
      <div class="rounded-3xl bg-white p-8 shadow-xl ring-1 ring-purple-100">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Constellation Marketing Studio</p>
        <h1 class="mt-4 text-4xl font-bold text-slate-900 md:text-5xl">
          Intelligent lifecycle marketing for teams that own revenue.
        </h1>
        <p class="mt-4 text-lg text-slate-600">
          Design sophisticated journeys, orchestrate deliverability, and stay compliant—without
          waiting on engineers. We fuse AI orchestration, drag-and-drop content, and enterprise IAM so
          you can ship revenue faster.
        </p>
        <div class="mt-6 flex flex-wrap gap-4">
          <RouterLink
            to="/register"
            class="rounded-full bg-purple-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-purple-200"
          >
            Launch Mission Control
          </RouterLink>
          <a href="#features" class="text-sm font-semibold text-emerald-600">See why teams switch →</a>
        </div>
        <dl class="mt-8 grid grid-cols-2 gap-6">
          <div v-for="stat in stats" :key="stat.label">
            <dt class="text-sm text-slate-500">{{ stat.label }}</dt>
            <dd class="text-2xl font-semibold text-slate-900">{{ stat.value }}</dd>
          </div>
        </dl>
      </div>
      <div class="flex flex-col justify-center space-y-6">
        <div class="rounded-3xl bg-slate-900 p-6 text-white shadow-2xl">
          <p class="text-sm uppercase tracking-[0.3em] text-purple-200">Profit Fuel</p>
          <h2 class="mt-3 text-3xl font-semibold">Connected journeys mean predictable revenue.</h2>
          <p class="mt-4 text-sm text-purple-100">
            Constellation turns campaign chaos into measurable outcomes. Marketers get instant
            insights, finance gets durable ROI, and security teams get the IAM posture they demand.
          </p>
        </div>
        <div class="flex gap-4">
          <div class="flex-1 rounded-2xl bg-white p-4 shadow-lg ring-1 ring-purple-100">
            <h3 class="text-base font-semibold text-slate-900">Landing → Trial</h3>
            <p class="text-sm text-slate-600">Guided walkthroughs convert 28% more trial users.</p>
          </div>
          <div class="flex-1 rounded-2xl bg-white p-4 shadow-lg ring-1 ring-purple-100">
            <h3 class="text-base font-semibold text-slate-900">Enterprise trust</h3>
            <p class="text-sm text-slate-600">SOC2, GDPR, and IAM readiness baked in.</p>
          </div>
        </div>
      </div>
    </header>

    <section id="features" class="mx-auto max-w-6xl px-6 py-12">
      <h2 class="text-3xl font-bold text-slate-900">Why revenue leaders choose us</h2>
      <div class="mt-8 grid gap-6 md:grid-cols-3">
        <article
          v-for="item in differentiators"
          :key="item.title"
          class="rounded-3xl bg-white p-6 shadow-lg ring-1 ring-purple-100"
        >
          <h3 class="text-xl font-semibold text-slate-900">{{ item.title }}</h3>
          <p class="mt-3 text-sm text-slate-600">{{ item.description }}</p>
        </article>
      </div>
    </section>

    <section class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-6 rounded-3xl bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-10 text-white md:flex-row">
      <div>
        <h3 class="text-2xl font-semibold">Ready to accelerate lifecycle marketing?</h3>
        <p class="mt-2 text-sm text-purple-100">
          Start with a free mission-control workspace, then upgrade when your team scales.
        </p>
      </div>
      <div class="flex gap-4">
        <RouterLink
          to="/register"
          class="rounded-full bg-white px-5 py-2 text-sm font-semibold text-purple-700"
        >
          Create Workspace
        </RouterLink>
        <RouterLink to="/login" class="rounded-full border border-white px-5 py-2 text-sm font-semibold">
          Sign in
        </RouterLink>
      </div>
    </section>
  </div>
</template>
