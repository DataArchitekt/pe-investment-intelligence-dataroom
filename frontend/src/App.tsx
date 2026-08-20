import { useEffect, useState } from 'react'
import { Layout } from './components/Layout'
import { DashboardPage } from './pages/DashboardPage'
import { DealPage } from './pages/DealPage'
import { DataRoomPage } from './pages/DataRoomPage'
import { api } from './services/api'
import type { Deal, Document } from './types/deal'

type View = 'dashboard' | 'deal' | 'data-room'
export default function App() {
  const [view, setView] = useState<View>('dashboard')
  const [deals, setDeals] = useState<Deal[]>([])
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null)
  const [documents, setDocuments] = useState<Document[]>([])
  const [error, setError] = useState('')
  useEffect(() => { api.listDeals().then(deals => { setDeals(deals); setSelectedDeal(deals[0] ?? null) }).catch(() => setError('The API is unavailable. Start the FastAPI backend and refresh.')) }, [])
  useEffect(() => { if (selectedDeal) api.listDocuments(selectedDeal.deal_id).then(setDocuments).catch(() => setError('Unable to load documents.')) }, [selectedDeal])
  const selectDeal = (deal: Deal) => { setSelectedDeal(deal); setView('deal') }
  return <Layout onNavigate={setView}>{error && <p className="error">{error}</p>}{view === 'dashboard' && <DashboardPage deals={deals} onSelect={selectDeal} />}{view === 'deal' && selectedDeal && <DealPage deal={selectedDeal} documentCount={documents.length} onOpenDataRoom={() => setView('data-room')} />}{view === 'data-room' && <DataRoomPage documents={documents} />}</Layout>
}
