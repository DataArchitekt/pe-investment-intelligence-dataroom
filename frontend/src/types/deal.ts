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
  file_size: number
  content_type: string
  original_file_name: string
  page_count: number
  processing_error: string | null
  chunk_count: number
  created_at: string
}

export interface DocumentChunk {
  chunk_id: string
  document_id: string
  deal_id: string
  chunk_text: string
  page_number: number | null
  section: string | null
  chunk_index: number
  token_count: number
  char_count: number
  created_at: string
}
