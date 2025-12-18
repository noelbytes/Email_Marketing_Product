import { useQuery } from '@tanstack/vue-query'
import { http } from '@/lib/httpClient'

type HealthResponse = {
  status: string
  service: string
  version: string
  timestamp: string
}

const healthQueryKey = ['healthz'] as const

export function useHealthQuery() {
  return useQuery({
    queryKey: healthQueryKey,
    queryFn: () => http<HealthResponse>('/healthz'),
    staleTime: 30_000,
  })
}
