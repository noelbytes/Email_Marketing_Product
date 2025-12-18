<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineEmits<{ 'link:clicked': [] }>()

const route = useRoute()
const auth = useAuthStore()

type NavItem = {
  label: string
  to: string
  name: string
  badge?: string
  permission?: string
}

const navItems: NavItem[] = [
  { label: 'Mission Control', to: '/app', name: 'dashboard' },
  { label: 'Campaigns', to: '/app/campaigns', name: 'campaigns', permission: 'campaigns.manage' },
  { label: 'Journeys', to: '/app/journeys', name: 'journeys', badge: '5', permission: 'journeys.build' },
  { label: 'Contacts', to: '/app/contacts', name: 'contacts', permission: 'journeys.build' },
  {
    label: 'Deliverability',
    to: '/app/deliverability',
    name: 'deliverability',
    permission: 'deliverability.view',
  },
  {
    label: 'Compliance Center',
    to: '/app/compliance',
    name: 'compliance',
    permission: 'compliance.manage',
  },
  {
    label: 'Template Builder',
    to: '/app/templates',
    name: 'templates',
    permission: 'templates.manage',
  },
]

const activeName = computed(() => route.name)
const visibleItems = computed(() =>
  navItems.filter((item) => !item.permission || auth.hasPermission(item.permission)),
)
</script>

<template>
  <nav class="nav">
    <RouterLink
      v-for="item in visibleItems"
      :key="item.name"
      :to="item.to"
      class="nav-item"
      :class="{ active: activeName === item.name }"
      @click="$emit('link:clicked')"
    >
      <span>{{ item.label }}</span>
      <span v-if="item.badge" class="badge">{{ item.badge }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  padding: 0.8rem 1rem;
  border-radius: 999px;
  color: var(--md-sys-color-on-surface);
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease, color 0.2s ease;
}

.nav-item.active {
  background: rgba(103, 80, 164, 0.15);
  color: var(--md-sys-color-primary);
}

.nav-item:hover {
  background: rgba(28, 27, 31, 0.06);
}

.badge {
  min-width: 30px;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  background: var(--md-sys-color-surface-variant);
  color: var(--md-sys-color-on-surface);
  text-align: center;
}
</style>
