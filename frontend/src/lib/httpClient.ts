const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

const TOKEN_KEY = 'constellation_token'

export class ApiError extends Error {
  status: number
  details?: unknown
  constructor(message: string, status: number, details?: unknown) {
    super(message)
    this.status = status
    this.details = details
  }
}

export function setAuthToken(token: string | null) {
  if (!token) {
    localStorage.removeItem(TOKEN_KEY)
    return
  }
  localStorage.setItem(TOKEN_KEY, token)
}

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const authToken = getAuthToken()
  const headers = new Headers(init?.headers)
  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  if (authToken && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${authToken}`)
  }
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers,
    ...init,
  })

  if (!response.ok) {
    const contentType = response.headers.get('content-type') ?? ''
    try {
      if (contentType.includes('application/json')) {
        const json = await response.json()
        const message = json?.error?.message ?? response.statusText
        const details = json?.error?.details
        throw new ApiError(message, response.status, details)
      }
      const body = await response.text()
      throw new ApiError(body || response.statusText, response.status)
    } catch (err) {
      if (err instanceof ApiError) throw err
      throw new ApiError(response.statusText, response.status)
    }
  }

  return (await response.json()) as T
}
