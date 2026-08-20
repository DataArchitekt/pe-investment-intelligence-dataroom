import type { Deal } from '../types/deal'

export function DashboardPage({ deals, onSelect }: { deals: Deal[]; onSelect: (deal: Deal) => void }) {
  return <section><p className="eyebrow">DEALS</p><h1>Deals</h1>{deals.map(deal => <button className="card deal-card" key={deal.deal_id} onClick={() => onSelect(deal)}><h2>{deal.name}</h2><p>{deal.industry}<br />{deal.geography}</p><div className="metrics"><span>${Number(deal.revenue).toLocaleString('en-US', { maximumFractionDigits: 0 })} Revenue</span><span>${Number(deal.ebitda).toLocaleString('en-US', { maximumFractionDigits: 0 })} EBITDA</span></div><span className="badge">{deal.deal_stage}</span></button>)}</section>
}
