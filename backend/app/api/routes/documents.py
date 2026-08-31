from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document import DocumentRead
from app.schemas.document_chunk import DocumentChunkRead
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.document_service import DocumentService

router = APIRouter(tags=["documents"])
document_service = DocumentService()
chunk_repository = DocumentChunkRepository()


@router.get("/documents/{document_id}", response_model=DocumentRead)
def get_document(document_id: str, db: Session = Depends(get_db)) -> DocumentRead:
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/documents/{document_id}/chunks", response_model=list[DocumentChunkRead])
def list_document_chunks(document_id: str, db: Session = Depends(get_db)) -> list[DocumentChunkRead]:
    if document_service.get_document(db, document_id) is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return chunk_repository.list_for_document(db, document_id)


@router.post("/documents/{document_id}/process", response_model=DocumentRead)
def reprocess_document(document_id: str, db: Session = Depends(get_db)) -> DocumentRead:
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document_service.reprocess_document(db, document)


@router.get("/documents/{document_id}/download")
def download_document(document_id: str, db: Session = Depends(get_db)) -> FileResponse:
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        file_path = document_service.get_document_file(document)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Stored file not found") from error
    return FileResponse(file_path, media_type=document.content_type, filename=document.file_name)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)) -> None:
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document_service.delete_document(db, document)
