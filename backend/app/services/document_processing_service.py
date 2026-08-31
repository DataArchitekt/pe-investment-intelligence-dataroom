import logging

from sqlalchemy.orm import Session

from app.integrations.contracts import StorageService
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.services.document_processors import ProcessingError, processor_for
from app.services.text_chunker import TextChunker

logger = logging.getLogger(__name__)


class DocumentProcessingService:
    def __init__(
        self,
        storage: StorageService,
        document_repository: DocumentRepository | None = None,
        chunk_repository: DocumentChunkRepository | None = None,
        chunker: TextChunker | None = None,
    ) -> None:
        self.storage = storage
        self.document_repository = document_repository or DocumentRepository()
        self.chunk_repository = chunk_repository or DocumentChunkRepository()
        self.chunker = chunker or TextChunker()

    def process(self, db: Session, document: Document) -> Document:
        document.status = DocumentStatus.PROCESSING
        document.processing_error = None
        self.document_repository.update(db, document)
        try:
            source = self.storage.get_file(document.file_path)
            pages = processor_for(source).extract(source)
            drafts = self.chunker.chunk(pages)
            if not drafts:
                raise ProcessingError("No chunks could be created from this document.")
            chunks = [
                DocumentChunk(
                    document_id=document.document_id,
                    deal_id=document.deal_id,
                    chunk_text=draft.chunk_text,
                    page_number=draft.page_number,
                    section=draft.section,
                    chunk_index=index,
                    token_count=draft.token_count,
                    char_count=draft.char_count,
                )
                for index, draft in enumerate(drafts)
            ]
            self.chunk_repository.replace_for_document(db, document.document_id, chunks)
            document.page_count = len(pages)
            document.status = DocumentStatus.PROCESSED
            document.processing_error = None
            return self.document_repository.update(db, document)
        except (ProcessingError, OSError, ValueError) as error:
            logger.warning("Processing failed for document %s: %s", document.document_id, error)
            self.chunk_repository.replace_for_document(db, document.document_id, [])
            document.status = DocumentStatus.FAILED
            document.processing_error = str(error)
            return self.document_repository.update(db, document)
        except Exception:
            logger.exception("Unexpected document processing failure for %s", document.document_id)
            self.chunk_repository.replace_for_document(db, document.document_id, [])
            document.status = DocumentStatus.FAILED
            document.processing_error = "Document processing failed. Please try again."
            return self.document_repository.update(db, document)
