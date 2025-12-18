<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import PrimaryNav from '@/components/navigation/PrimaryNav.vue'

const auth = useAuthStore()
const router = useRouter()
const showDrawer = ref(false)
const isDesktop = ref(false)

function handleSignOut() {
  auth.logout()
  router.push({ name: 'login' })
}

function toggleDrawer() {
  if (!isDesktop.value) {
    showDrawer.value = !showDrawer.value
  }
}

function closeDrawer() {
  if (!isDesktop.value) {
    showDrawer.value = false
  }
}

function evaluateMedia(query: MediaQueryList | MediaQueryListEvent) {
  isDesktop.value = query.matches
  if (query.matches) {
    showDrawer.value = false
  }
}

let mq: MediaQueryList | null = null

onMounted(() => {
  mq = window.matchMedia('(min-width: 960px)')
  evaluateMedia(mq)
  mq.addEventListener('change', evaluateMedia)
})

onUnmounted(() => {
  mq?.removeEventListener('change', evaluateMedia)
})
</script>

<template>
  <div class="shell">
    <button class="nav-toggle" type="button" aria-label="Open navigation" @click="toggleDrawer">
      ☰
    </button>
    <aside :class="{ open: isDesktop || showDrawer }">
      <div class="brand">
        <span class="badge">β</span>
        <div>
          <p class="brand-title">Constellation</p>
          <small>Marketing Studio</small>
        </div>
      </div>
      <PrimaryNav @link:clicked="closeDrawer" />
      <footer>
        <p class="supporting">Workspace</p>
        <p class="workspace">
          {{ auth.user?.organization_id ? `Workspace #${auth.user?.organization_id}` : 'Workspace' }}
        </p>
      </footer>
    </aside>

    <section class="content">
      <header class="top-bar surface">
        <div>
          <p class="supporting">Customer Intelligence</p>
          <h1>Lifecycle Command</h1>
        </div>
        <div class="session">
          <div>
            <p class="workspace">{{ auth.user?.first_name || auth.user?.email }}</p>
            <small>{{ auth.user?.email }}</small>
          </div>
          <button class="text-button" type="button" @click="handleSignOut">Sign out</button>
        </div>
      </header>
      <main>
        <RouterView />
      </main>
    </section>
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--md-sys-color-background);
}

.nav-toggle {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  font-size: 1.5rem;
  box-shadow: var(--md-shadow);
  z-index: 30;
  cursor: pointer;
}

aside {
  position: fixed;
  inset: 0 auto 0 0;
  width: 290px;
  padding: 1.5rem;
  background: var(--md-sys-color-surface);
  border-right: 1px solid var(--md-sys-color-surface-variant);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 20;
}

aside.open {
  transform: translateX(0);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-title {
  font-weight: 600;
}

.badge {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: linear-gradient(120deg, #bb86fc, var(--md-sys-color-primary));
  color: var(--md-sys-color-on-primary);
  display: grid;
  place-items: center;
  font-weight: 600;
}

footer {
  margin-top: auto;
  padding-top: 1.5rem;
  border-top: 1px solid var(--md-sys-color-surface-variant);
}

.supporting {
  text-transform: uppercase;
  font-size: 0.75rem;
  color: var(--md-sys-color-on-surface-variant);
  letter-spacing: 0.2em;
}

.workspace {
  font-weight: 600;
}

.content {
  padding: 1rem clamp(1rem, 4vw, 5rem);
  padding-top: 5rem;
  margin-left: 0;
  flex: 1;
  min-width: 0;
}

.top-bar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.session {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.text-button {
  border: none;
  background: transparent;
  color: var(--md-sys-color-primary);
  font-weight: 600;
  cursor: pointer;
}

main {
  padding-bottom: 3rem;
}

@media (min-width: 960px) {
  .shell {
    flex-direction: row;
  }
  .nav-toggle {
    display: none;
  }

  aside {
    position: sticky;
    transform: translateX(0);
    height: 100vh;
  }

  .content {
    padding-top: 2rem;
  }

  .top-bar {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
