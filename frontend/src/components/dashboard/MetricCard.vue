<script setup lang="ts">
type Metric = {
  label: string
  value: string
  caption: string
  trend?: number
}

defineProps<Metric>()
</script>

<template>
  <article class="card">
    <p class="label">{{ label }}</p>
    <div class="value-row">
      <h3>{{ value }}</h3>
      <span v-if="trend" :class="['trend', trend > 0 ? 'up' : 'down']">
        {{ trend > 0 ? '+' : '' }}{{ trend }}%
      </span>
    </div>
    <p class="caption">{{ caption }}</p>
  </article>
</template>

<style scoped>
.card {
  background: var(--md-sys-color-surface);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid var(--md-sys-color-surface-variant);
  box-shadow: var(--md-shadow);
}

.label {
  text-transform: uppercase;
  font-size: 0.75rem;
  color: var(--md-sys-color-on-surface-variant);
}

.value-row {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

h3 {
  font-size: 2rem;
  color: var(--md-sys-color-on-surface);
  margin: 0;
}

.caption {
  color: var(--md-sys-color-on-surface-variant);
  margin-top: 0.25rem;
}

.trend {
  font-size: 0.9rem;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
}

.trend.up {
  color: #0f766e;
  background: rgba(16, 185, 129, 0.15);
}

.trend.down {
  color: #b91c1c;
  background: rgba(239, 68, 68, 0.12);
}
</style>
