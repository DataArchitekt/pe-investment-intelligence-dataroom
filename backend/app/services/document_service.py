from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, repository: DocumentRepository | None = None) -> None:
        self.repository = repository or DocumentRepository()

    def list_documents_for_deal(self, db: Session, deal_id: str) -> list[Document]:
        return self.repository.list_for_deal(db, deal_id)

    def get_document(self, db: Session, document_id: str) -> Document | None:
        return self.repository.get_by_id(db, document_id)
