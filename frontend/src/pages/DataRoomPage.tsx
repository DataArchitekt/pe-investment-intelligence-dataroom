import type { Document } from '../types/deal'

const categories = ['Financial', 'Commercial', 'Legal', 'HR', 'Operations', 'Contracts', 'Corporate', 'Other']
export function DataRoomPage({ documents }: { documents: Document[] }) {
  return <section><p className="eyebrow">DATA ROOM</p><h1>Data Room</h1><div className="categories">{categories.map(category => <div className="category" key={category}><span>{category}</span><strong>{documents.filter(document => document.category === category).length}</strong></div>)}</div><div className="documents"><h2>Documents</h2>{documents.length === 0 ? <p>No documents uploaded yet.</p> : <ul>{documents.map(document => <li key={document.document_id}>{document.file_name}</li>)}</ul>}</div></section>
}
