from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def list_for_deal(self, db: Session, deal_id: str) -> list[Document]:
        query = select(Document).where(Document.deal_id == deal_id).order_by(Document.created_at)
        return list(db.scalars(query))

    def get_by_id(self, db: Session, document_id: str) -> Document | None:
        return db.get(Document, document_id)
