import { createRouter, createWebHistory } from 'vue-router'
import AppShell from '@/layouts/AppShell.vue'
import DashboardView from '@/views/DashboardView.vue'
import JourneysView from '@/views/JourneysView.vue'
import DeliverabilityView from '@/views/DeliverabilityView.vue'
import ComplianceView from '@/views/ComplianceView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LandingView from '@/views/LandingView.vue'
import UnauthorizedView from '@/views/UnauthorizedView.vue'
import { useAuthStore } from '@/stores/auth'
import { getAuthToken } from '@/lib/httpClient'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/app',
      component: AppShell,
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'dashboard', component: DashboardView },
        {
          path: 'journeys',
          name: 'journeys',
          component: JourneysView,
          meta: { permission: 'journeys.build' },
        },
        {
          path: 'campaigns',
          name: 'campaigns',
          component: () => import('@/views/CampaignsView.vue'),
          meta: { permission: 'campaigns.manage' },
        },
        {
          path: 'contacts',
          name: 'contacts',
          component: () => import('@/views/ContactsView.vue'),
          meta: { permission: 'journeys.build' },
        },
        {
          path: 'deliverability',
          name: 'deliverability',
          component: DeliverabilityView,
          meta: { permission: 'deliverability.view' },
        },
        {
          path: 'compliance',
          name: 'compliance',
          component: ComplianceView,
          meta: { permission: 'compliance.manage' },
        },
        {
          path: 'templates',
          name: 'templates',
          component: () => import('@/views/TemplateBuilderView.vue'),
          meta: { permission: 'templates.manage' },
        },
      ],
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: UnauthorizedView,
    },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.isAuthenticated && getAuthToken()) {
    try {
      await auth.loadProfile()
    } catch {
      auth.logout()
    }
  }
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  if (requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if ((to.name === 'login' || to.name === 'landing') && auth.isAuthenticated) {
    return { path: '/app' }
  }
  const permission = to.meta.permission as string | undefined
  if (permission && !auth.hasPermission(permission)) {
    return { name: 'unauthorized' }
  }
  return true
})

export default router
