import type { Deal } from '../types/deal'

export function DealPage({ deal, documentCount, onOpenDataRoom }: { deal: Deal; documentCount: number; onOpenDataRoom: () => void }) {
  return <section><p className="eyebrow">DEAL</p><h1>{deal.name.toUpperCase()}</h1><p className="subtitle">{deal.industry}<br />{deal.geography}</p><div className="metrics large"><span>${Number(deal.revenue).toLocaleString('en-US', { maximumFractionDigits: 0 })} Revenue</span><span>${Number(deal.ebitda).toLocaleString('en-US', { maximumFractionDigits: 0 })} EBITDA</span></div><div className="stage"><small>DEAL STAGE</small><strong>{deal.deal_stage}</strong></div><button className="card data-room-link" onClick={onOpenDataRoom}><h2>Data Room</h2><p>{documentCount} Documents</p><span>Open data room →</span></button></section>
}
