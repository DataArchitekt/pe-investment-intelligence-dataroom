from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    def list_for_document(self, db: Session, document_id: str) -> list[DocumentChunk]:
        query = select(DocumentChunk).where(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index)
        return list(db.scalars(query))

    def list_for_deal(self, db: Session, deal_id: str) -> list[DocumentChunk]:
        query = select(DocumentChunk).where(DocumentChunk.deal_id == deal_id).order_by(DocumentChunk.chunk_index)
        return list(db.scalars(query))

    def replace_for_document(self, db: Session, document_id: str, chunks: list[DocumentChunk]) -> None:
        db.execute(delete(DocumentChunk).where(DocumentChunk.document_id == document_id))
        db.add_all(chunks)
        db.commit()
