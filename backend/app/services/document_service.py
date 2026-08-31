import mimetypes
from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.integrations.storage.local import LocalStorageService
from app.models.document import Document, DocumentCategory, DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.services.document_processing_service import DocumentProcessingService

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".xlsx"}


class DocumentUploadError(ValueError):
    pass


class DocumentService:
    def __init__(
        self,
        repository: DocumentRepository | None = None,
        storage: LocalStorageService | None = None,
        processing_service: DocumentProcessingService | None = None,
    ) -> None:
        self.repository = repository or DocumentRepository()
        self.storage = storage or LocalStorageService()
        self.processing_service = processing_service or DocumentProcessingService(
            self.storage, self.repository
        )

    def list_documents_for_deal(self, db: Session, deal_id: str) -> list[Document]:
        return self.repository.list_for_deal(db, deal_id)

    def get_document(self, db: Session, document_id: str) -> Document | None:
        return self.repository.get_by_id(db, document_id)

    def upload_document(
        self, db: Session, deal_id: str, category: DocumentCategory, file_name: str, content: bytes
    ) -> Document:
        extension = Path(file_name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise DocumentUploadError("Unsupported file type. Allowed: PDF, DOCX, TXT, XLSX.")
        if not content:
            raise DocumentUploadError("The selected file is empty.")

        safe_path = self.storage.save_file(deal_id, category.value, file_name, content)
        stored_name = Path(safe_path).name
        try:
            document = self.repository.create(
                db,
                Document(
                    document_id=f"DOC-{uuid4().hex[:16].upper()}",
                    deal_id=deal_id,
                    file_name=stored_name,
                    original_file_name=Path(file_name).name,
                    category=category,
                    file_path=safe_path,
                    status=DocumentStatus.PENDING,
                    file_size=len(content),
                    content_type=mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
                ),
            )
            return self.processing_service.process(db, document)
        except Exception:
            self.storage.delete_file(safe_path)
            raise

    def get_document_file(self, document: Document) -> Path:
        return self.storage.get_file(document.file_path)

    def delete_document(self, db: Session, document: Document) -> None:
        self.storage.delete_file(document.file_path)
        self.repository.delete(db, document)

    def reprocess_document(self, db: Session, document: Document) -> Document:
        return self.processing_service.process(db, document)
