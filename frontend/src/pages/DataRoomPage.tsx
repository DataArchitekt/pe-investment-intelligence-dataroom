import { FormEvent, useState } from 'react'
import { api } from '../services/api'
import type { Deal, Document, DocumentChunk } from '../types/deal'

const categories = ['Financial', 'Commercial', 'Legal', 'HR', 'Operations', 'Contracts', 'Corporate', 'Other']
const acceptedTypes = '.pdf,.docx,.txt,.xlsx'

function formatSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function DataRoomPage({ deal, documents, onDocumentsChanged }: { deal: Deal; documents: Document[]; onDocumentsChanged: (documents: Document[]) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [category, setCategory] = useState(categories[0])
  const [isUploading, setIsUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null)
  const [chunks, setChunks] = useState<DocumentChunk[]>([])

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!file) { setError('Choose a document to upload.'); return }
    setIsUploading(true); setError(''); setMessage('')
    try {
      const uploadedDocument = await api.uploadDocument(deal.deal_id, file, category)
      onDocumentsChanged([...documents, uploadedDocument])
      setFile(null)
      const input = document.getElementById('document-file') as HTMLInputElement | null
      if (input) input.value = ''
      setMessage(`${uploadedDocument.file_name} uploaded. It is pending processing.`)
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : 'Upload failed. Please try again.')
    } finally { setIsUploading(false) }
  }

  async function remove(document: Document) {
    if (!window.confirm(`Delete ${document.file_name}?`)) return
    setError(''); setMessage('')
    try {
      await api.deleteDocument(document.document_id)
      onDocumentsChanged(documents.filter(item => item.document_id !== document.document_id))
      setMessage(`${document.file_name} deleted.`)
    } catch { setError('Delete failed. Please try again.') }
  }

  async function showDetails(document: Document) {
    setError(''); setSelectedDocument(document)
    try { setChunks(await api.listChunks(document.document_id)) }
    catch { setError('Unable to load document chunks.') }
  }

  async function reprocess(document: Document) {
    setError(''); setMessage('')
    try {
      const updated = await api.reprocessDocument(document.document_id)
      onDocumentsChanged(documents.map(item => item.document_id === updated.document_id ? updated : item))
      setSelectedDocument(updated)
      setChunks(await api.listChunks(updated.document_id))
      setMessage(`${updated.file_name} processing completed with status: ${updated.status}.`)
    } catch { setError('Reprocessing failed. Please try again.') }
  }

  return <section>
    <p className="eyebrow">{deal.company_name.toUpperCase()}</p><h1>Data Room</h1>
    <div className="categories">{categories.map(item => <div className="category" key={item}><span>{item}</span><strong>{documents.filter(document => document.category === item).length}</strong></div>)}</div>
    <div className="documents"><div className="section-heading"><div><h2>Documents</h2><p>{documents.length} document{documents.length === 1 ? '' : 's'}</p></div></div>
      <form className="upload-form" onSubmit={submit}>
        <label>File<input id="document-file" type="file" accept={acceptedTypes} onChange={event => setFile(event.target.files?.[0] ?? null)} /></label>
        <label>Category<select value={category} onChange={event => setCategory(event.target.value)}>{categories.map(item => <option key={item}>{item}</option>)}</select></label>
        <button className="primary" type="submit" disabled={isUploading}>{isUploading ? 'Uploading…' : '+ Upload Document'}</button>
      </form>
      {message && <p className="notice success">{message}</p>}{error && <p className="notice error">{error}</p>}
      {documents.length === 0 ? <div className="empty-state"><p>No documents in the Data Room yet.</p><span>Upload seller documents to begin building the deal intelligence workspace.</span></div> : <div className="table-wrap"><table><thead><tr><th>Document</th><th>Category</th><th>Status</th><th>Size</th><th>Uploaded</th><th>Actions</th></tr></thead><tbody>{documents.map(document => <tr key={document.document_id}><td>{document.file_name}</td><td>{document.category}</td><td><span className="badge">{document.status}</span></td><td>{formatSize(document.file_size)}</td><td>{new Date(document.created_at).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}</td><td className="actions"><button className="link-button" onClick={() => showDetails(document)}>Details</button><a href={api.downloadUrl(document.document_id)} target="_blank" rel="noreferrer">Open / Download</a><button onClick={() => remove(document)}>Delete</button></td></tr>)}</tbody></table></div>}
      {selectedDocument && <aside className="document-details"><div className="detail-heading"><h2>{selectedDocument.file_name}</h2><button onClick={() => setSelectedDocument(null)}>Close</button></div><dl><dt>Category</dt><dd>{selectedDocument.category}</dd><dt>Status</dt><dd><span className="badge">{selectedDocument.status}</span></dd><dt>File size</dt><dd>{formatSize(selectedDocument.file_size)}</dd><dt>Uploaded</dt><dd>{new Date(selectedDocument.created_at).toLocaleDateString()}</dd><dt>Pages / Chunks</dt><dd>{selectedDocument.page_count} / {selectedDocument.chunk_count}</dd><dt>Summary</dt><dd>{selectedDocument.summary ?? 'Not available yet.'}</dd></dl>{selectedDocument.processing_error && <p className="notice error">{selectedDocument.processing_error}</p>}<div className="detail-actions"><button className="primary" onClick={() => reprocess(selectedDocument)}>Reprocess</button><a href={api.downloadUrl(selectedDocument.document_id)} target="_blank" rel="noreferrer">Open / Download</a></div>{chunks.length > 0 && <details><summary>View extracted chunks ({chunks.length})</summary>{chunks.map(chunk => <article className="chunk" key={chunk.chunk_id}><small>{chunk.page_number ? `Page ${chunk.page_number}` : 'No page number'}{chunk.section ? ` · ${chunk.section}` : ''}</small><p>{chunk.chunk_text}</p></article>)}</details>}</aside>}
    </div>
  </section>
}
