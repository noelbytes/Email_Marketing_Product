<script setup lang="ts">
const regions = [
  { region: 'NA', inbox: 97.1, trend: '+1.3%', alerts: 0 },
  { region: 'EU', inbox: 95.6, trend: '-0.4%', alerts: 1 },
  { region: 'APAC', inbox: 93.8, trend: '+0.9%', alerts: 0 },
]
</script>

<template>
  <section class="deliverability">
    <header>
      <div>
        <h2>Deliverability Center</h2>
        <p>Seed list modeling, BIMI/SPF/DKIM monitoring, AI remediation</p>
      </div>
      <button type="button">Run Inbox Test</button>
    </header>
    <div class="grid">
      <article>
        <p class="eyebrow">Authentication</p>
        <h3>Compliant</h3>
        <ul>
          <li><span>BIMI</span><strong>Verified</strong></li>
          <li><span>SPF</span><strong>Aligned</strong></li>
          <li><span>DMARC</span><strong>Strict</strong></li>
        </ul>
      </article>
      <article>
        <p class="eyebrow">Engagement Baseline</p>
        <h3>51.7%</h3>
        <p>Rolling 30-day unique open rate</p>
      </article>
      <article>
        <p class="eyebrow">Fatigue Watchlist</p>
        <h3>312 contacts</h3>
        <p>Automatically throttled</p>
      </article>
    </div>
    <table>
      <thead>
        <tr>
          <th>Region</th>
          <th>Inbox Placement</th>
          <th>Trend</th>
          <th>Alerts</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in regions" :key="row.region">
          <td>{{ row.region }}</td>
          <td>{{ row.inbox }}%</td>
          <td>{{ row.trend }}</td>
          <td>
            <span class="status-pill" :class="{ alert: row.alerts > 0 }">
              {{ row.alerts }} alerts
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.deliverability {
  background: var(--md-sys-color-surface);
  border-radius: 24px;
  padding: clamp(1rem, 3vw, 2rem);
  border: 1px solid var(--md-sys-color-surface-variant);
  box-shadow: var(--md-shadow);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

button {
  border: none;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  padding: 0.8rem 1.4rem;
  border-radius: 16px;
  cursor: pointer;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

article {
  border: 1px solid var(--md-sys-color-surface-variant);
  border-radius: 20px;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.9);
}

.eyebrow {
  text-transform: uppercase;
  font-size: 0.75rem;
  color: var(--md-sys-color-on-surface-variant);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.85rem 0.5rem;
  text-align: left;
}

th {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.85rem;
  text-transform: uppercase;
}

tbody tr {
  border-top: 1px solid var(--card-border);
}

.status-pill {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.12);
  color: #065f46;
}

.status-pill.alert {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}
</style>
