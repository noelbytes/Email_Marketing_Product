import { defineStore } from 'pinia'
import { http, setAuthToken, getAuthToken } from '@/lib/httpClient'

type UserProfile = {
  id: number
  email: string
  first_name?: string | null
  last_name?: string | null
  organization_id: number
  roles: string[]
}

type LoginPayload = {
  email: string
  password: string
  organization?: string
}

type RegisterPayload = LoginPayload & {
  first_name?: string
  last_name?: string
}
type LoginResponse = {
  access_token: string
  token_type: string
  user: UserProfile
  roles: string[]
  permissions: string[]
}

type ProfileResponse = {
  user: UserProfile
  roles: string[]
  permissions: string[]
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as UserProfile | null,
    roles: [] as string[],
    permissions: [] as string[],
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.user),
    hasPermission: (state) => (permission: string) => state.permissions.includes('*') || state.permissions.includes(permission),
  },
  actions: {
    async register(payload: RegisterPayload) {
      this.loading = true
      try {
        const response = await http<LoginResponse>('/auth/register', {
          method: 'POST',
          body: JSON.stringify(payload),
        })
        setAuthToken(response.access_token)
        this.user = response.user
        this.roles = response.roles
        this.permissions = response.permissions
      } finally {
        this.loading = false
      }
    },
    async login(payload: LoginPayload) {
      this.loading = true
      try {
        const response = await http<LoginResponse>('/auth/login', {
          method: 'POST',
          body: JSON.stringify(payload),
        })
        setAuthToken(response.access_token)
        this.user = response.user
        this.roles = response.roles
        this.permissions = response.permissions
      } finally {
        this.loading = false
      }
    },
    async loadProfile() {
      const token = getAuthToken()
      if (!token) {
        return
      }
      const profile = await http<ProfileResponse>('/auth/me')
      this.user = profile.user
      this.roles = profile.roles
      this.permissions = profile.permissions
    },
    logout() {
      setAuthToken(null)
      this.user = null
      this.roles = []
      this.permissions = []
    },
  },
})
