<script setup lang="ts">
import { computed } from 'vue'
import MetricCard from '@/components/dashboard/MetricCard.vue'
import { useHealthQuery } from '@/composables/useHealth'

const metrics = [
  {
    label: 'Active Journeys',
    value: '18',
    caption: '4 launching next 7 days',
    trend: 8.3,
  },
  {
    label: 'Weekly Send Volume',
    value: '4.7M',
    caption: 'Across 3 brands',
    trend: 3.2,
  },
  {
    label: 'Revenue Influence',
    value: '$1.94M',
    caption: 'Last 30 days, attributed',
    trend: 11.4,
  },
]

const { data, isPending, isError } = useHealthQuery()
const apiStatus = computed(() => {
  if (isPending.value) return 'Checking API heartbeat...'
  if (isError.value) return 'API unavailable'
  return `API ${data.value?.service} • v${data.value?.version}`
})
</script>

<template>
  <section class="grid">
    <MetricCard
      v-for="metric in metrics"
      :key="metric.label"
      v-bind="metric"
    />
    <article class="canvas">
      <div v-if="isPending" class="skeleton-block" aria-busy="true"></div>
      <template v-else>
        <div class="canvas-header">
          <div>
            <p class="eyebrow">Journey Health</p>
            <h2>Intelligent orchestration</h2>
          </div>
          <button type="button">View Builder</button>
        </div>
        <ul class="journey-list">
          <li>
            <p>Repeat purchase Reactor</p>
            <small>Predictive send window open in 2 hrs</small>
            <span class="status good">On Track</span>
          </li>
          <li>
            <p>VIP Reactivation</p>
            <small>Fatigue guard triggered on branch B</small>
            <span class="status warn">Action Needed</span>
          </li>
          <li>
            <p>Compliance watchdog</p>
            <small>Auto-suppressed 34 high-risk emails</small>
            <span class="status good">Protected</span>
          </li>
        </ul>
      </template>
    </article>
    <article class="canvas system">
      <header>
        <p class="eyebrow">Platform Signal</p>
        <h2>Status & Integrations</h2>
      </header>
      <dl v-if="!isPending">
        <div>
          <dt>Core services</dt>
          <dd>{{ apiStatus }}</dd>
        </div>
        <div>
          <dt>Integrations</dt>
          <dd>Shopify, Snowflake, Salesforce (live)</dd>
        </div>
        <div>
          <dt>Deliverability</dt>
          <dd>Seed inbox placement 96.4%</dd>
        </div>
      </dl>
      <div v-else class="skeleton-block" aria-busy="true"></div>
    </article>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.canvas {
  grid-column: span 2;
  background: var(--md-sys-color-surface);
  border-radius: 24px;
  padding: clamp(1rem, 3vw, 1.75rem);
  border: 1px solid var(--md-sys-color-surface-variant);
  box-shadow: var(--md-shadow);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.canvas-header button {
  border: none;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: 20px;
  padding: 0.6rem 1.4rem;
  cursor: pointer;
}

.journey-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.journey-list li {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.5rem;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid var(--card-border);
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.05), rgba(99, 102, 241, 0));
}

.journey-list small {
  color: var(--md-sys-color-on-surface-variant);
}

.status {
  font-size: 0.75rem;
  padding: 0.2rem 0.75rem;
  border-radius: 999px;
}

.status.good {
  background: rgba(16, 185, 129, 0.15);
  color: #0f5132;
}

.status.warn {
  background: rgba(249, 115, 22, 0.15);
  color: #7c2d12;
}

.system dl {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.system dt {
  text-transform: uppercase;
  font-size: 0.75rem;
  color: var(--md-sys-color-on-surface-variant);
}

.system dd {
  font-weight: 600;
  color: var(--md-sys-color-on-surface);
}

.skeleton-block {
  height: 180px;
  border-radius: 18px;
  background: linear-gradient(
    90deg,
    rgba(226, 220, 239, 0.6) 0%,
    rgba(255, 255, 255, 0.9) 50%,
    rgba(226, 220, 239, 0.6) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 0% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 900px) {
  .canvas {
    grid-column: span 1;
  }
}
</style>
