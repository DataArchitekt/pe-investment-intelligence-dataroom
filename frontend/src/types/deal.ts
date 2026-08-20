export interface Deal {
  deal_id: string
  name: string
  company_name: string
  industry: string
  geography: string
  revenue: string
  ebitda: string
  deal_stage: string
  created_at: string
}

export interface Document {
  document_id: string
  deal_id: string
  file_name: string
  category: string
  file_path: string
  status: string
  summary: string | null
  created_at: string
}
