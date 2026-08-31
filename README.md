# PE Investment Intelligence Data Room MVP

An AI-powered Deal Data Room that turns seller documents into investment intelligence for a PE deal team.

## Current MVP phase

**Day 2 — Document Processing.** This phase adds local PDF/DOCX/TXT extraction, deterministic chunking, and chunk metadata. No Azure service is required.

## Architecture

```text
React Frontend
      ↓
FastAPI API
      ↓
Services
      ↓
Repositories
      ↓
SQLite
```

Future provider adapters will preserve this business-layer boundary:

```text
React → FastAPI → Services → Repositories
                         ↓
          SQLite | Azure Blob | Azure AI Search → Azure OpenAI
```

## Local setup

### 1. Environment configuration

Copy `.env.example` to `.env` if you want to override settings. All Azure variables are optional placeholders and must remain empty for this phase. The local SQLite database is created automatically at `data/app.db`.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`; API docs are at `/docs`.

### 3. Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the displayed Vite URL (normally `http://localhost:5173`). The UI reads the API at `http://localhost:8000` by default. Set `VITE_API_URL` in `frontend/.env` only if needed.

### 4. Tests

```bash
pytest
```

## Included API

- `GET /health`
- `GET /api/deals`
- `GET /api/deals/{deal_id}`
- `POST /api/deals`
- `GET /api/deals/{deal_id}/documents`
- `POST /api/deals/{deal_id}/documents` (multipart `file` + `category`)
- `GET /api/documents/{document_id}`
- `GET /api/documents/{document_id}/chunks`
- `POST /api/documents/{document_id}/process`
- `GET /api/documents/{document_id}/download`
- `DELETE /api/documents/{document_id}`

On first start, the database seeds `ABC-HYD-001` / ABC Hydraulic Systems. Every document requires a `deal_id`, establishing the scope required for later deal-filtered retrieval.

## Day 1 capabilities

- Local upload and storage for PDF, DOCX, TXT, and XLSX files (25 MB default limit)
- Manual category selection, metadata, file size, upload date, and `Pending` processing status
- Per-deal document listings, category counts, download/open, and deletion
- Filename sanitisation and duplicate preservation (`file (1).pdf`), with no uploaded files committed to Git

**Current storage:** local filesystem under `data/documents/<deal-id>/<category>/`.

**Future storage:** Azure Blob / ADLS Gen2 through a replacement storage adapter. Azure infrastructure is intentionally not connected in this phase.

## Day 2 capabilities

After upload, documents are processed synchronously for local MVP-sized files:

```text
Document → extraction → conservative text cleaning → word-based chunks → SQLite → Processed
```

- PDF extraction preserves one-based page numbers.
- DOCX paragraphs, headings, and basic table rows are retained where available; Word page numbers remain unknown.
- TXT is supported as a single logical document.
- Chunks retain `deal_id`, `document_id`, source page, section (when available), sequential index, word-based token approximation, and character count.
- XLSX uploads remain supported for storage but deliberately move to `Failed` processing with a clear message; spreadsheet extraction is deferred.

No embeddings, vector search, Azure services, RAG, or AI summaries are implemented.

## Future components — not implemented

The code contains abstract contracts for `StorageService`, `DocumentProcessor`, `EmbeddingService`, `LLMService`, and `VectorSearchService`. Future work may supply Azure Blob/ADLS, Azure OpenAI, and Azure AI Search adapters.

The following are explicitly out of scope for Day 1: document parsing, ADLS/Blob, Azure OpenAI, Azure AI Search, embeddings, vector search, RAG, citations, and diligence intelligence.
