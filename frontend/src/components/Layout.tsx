import type { ReactNode } from 'react'

type View = 'dashboard' | 'deal' | 'data-room'

export function Layout({ children, onNavigate }: { children: ReactNode; onNavigate: (view: View) => void }) {
  return <><header><button className="brand" onClick={() => onNavigate('dashboard')}>PE INVESTMENT INTELLIGENCE</button><nav><button onClick={() => onNavigate('dashboard')}>Dashboard</button><button onClick={() => onNavigate('dashboard')}>Deals</button></nav></header><main>{children}</main></>
}
