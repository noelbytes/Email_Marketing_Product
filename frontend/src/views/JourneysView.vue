<script setup lang="ts">
const schedules = [
  {
    name: 'New subscriber concierge',
    trigger: 'Segment entry',
    goal: 'First purchase',
    status: 'live',
  },
  {
    name: 'High-risk churn defense',
    trigger: 'Signal: LTV drop',
    goal: 'Reactivation',
    status: 'testing',
  },
  {
    name: 'Wholesale enablement',
    trigger: 'Salesforce opportunity',
    goal: 'Close rate',
    status: 'draft',
  },
]
</script>

<template>
  <section class="journeys">
    <header>
      <div>
        <h2>Journeys</h2>
        <p>Visual orchestration with AI guardrails</p>
      </div>
      <button type="button">New Journey</button>
    </header>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Trigger</th>
          <th>Primary Goal</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="journey in schedules" :key="journey.name">
          <td>{{ journey.name }}</td>
          <td>{{ journey.trigger }}</td>
          <td>{{ journey.goal }}</td>
          <td>
            <span class="status-pill" :class="journey.status">{{ journey.status }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.journeys {
  background: var(--md-sys-color-surface);
  border-radius: 24px;
  padding: clamp(1rem, 3vw, 2rem);
  border: 1px solid var(--md-sys-color-surface-variant);
  box-shadow: var(--md-shadow);
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

button {
  border: none;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  padding: 0.8rem 1.5rem;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.9rem 0.5rem;
  text-align: left;
}

th {
  font-size: 0.85rem;
  text-transform: uppercase;
  color: var(--md-sys-color-on-surface-variant);
}

tbody tr {
  border-top: 1px solid var(--card-border);
}

.status-pill {
  padding: 0.2rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.status-pill.live {
  background: rgba(16, 185, 129, 0.15);
  color: #065f46;
}

.status-pill.testing {
  background: rgba(249, 115, 22, 0.15);
  color: #7c2d12;
}

.status-pill.draft {
  background: rgba(148, 163, 184, 0.3);
  color: var(--md-sys-color-on-surface-variant);
}
</style>
