import type { Deal, Document } from '../types/deal'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`)
  if (!response.ok) throw new Error(await errorMessage(response))
  return response.json() as Promise<T>
}

async function errorMessage(response: Response): Promise<string> {
  const body = await response.json().catch(() => null) as { detail?: string } | null
  return body?.detail ?? `Request failed (${response.status})`
}

export const api = {
  listDeals: () => request<Deal[]>('/api/deals'),
  getDeal: (dealId: string) => request<Deal>(`/api/deals/${dealId}`),
  listDocuments: (dealId: string) => request<Document[]>(`/api/deals/${dealId}/documents`),
  uploadDocument: async (dealId: string, file: File, category: string): Promise<Document> => {
    const form = new FormData()
    form.append('file', file)
    form.append('category', category)
    const response = await fetch(`${API_URL}/api/deals/${dealId}/documents`, { method: 'POST', body: form })
    if (!response.ok) throw new Error(await errorMessage(response))
    return response.json() as Promise<Document>
  },
  deleteDocument: async (documentId: string): Promise<void> => {
    const response = await fetch(`${API_URL}/api/documents/${documentId}`, { method: 'DELETE' })
    if (!response.ok) throw new Error(await errorMessage(response))
  },
  downloadUrl: (documentId: string) => `${API_URL}/api/documents/${documentId}/download`,
}
