import type { Deal, Document } from '../types/deal'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`)
  if (!response.ok) throw new Error(`Request failed (${response.status})`)
  return response.json() as Promise<T>
}

export const api = {
  listDeals: () => request<Deal[]>('/api/deals'),
  getDeal: (dealId: string) => request<Deal>(`/api/deals/${dealId}`),
  listDocuments: (dealId: string) => request<Document[]>(`/api/deals/${dealId}/documents`),
}
