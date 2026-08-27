import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.models.document import DocumentCategory
from app.schemas.deal import DealCreate, DealRead
from app.schemas.document import DocumentRead
from app.services.deal_service import DealService
from app.services.document_service import DocumentService, DocumentUploadError

router = APIRouter(tags=["deals"])
logger = logging.getLogger(__name__)
deal_service = DealService()
document_service = DocumentService()


@router.get("/deals", response_model=list[DealRead])
def list_deals(db: Session = Depends(get_db)) -> list[DealRead]:
    return deal_service.list_deals(db)


@router.get("/deals/{deal_id}", response_model=DealRead)
def get_deal(deal_id: str, db: Session = Depends(get_db)) -> DealRead:
    deal = deal_service.get_deal(db, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("/deals", response_model=DealRead, status_code=status.HTTP_201_CREATED)
def create_deal(payload: DealCreate, db: Session = Depends(get_db)) -> DealRead:
    if deal_service.get_deal(db, payload.deal_id):
        raise HTTPException(status_code=409, detail="A deal with this ID already exists")
    return deal_service.create_deal(db, payload)


@router.get("/deals/{deal_id}/documents", response_model=list[DocumentRead])
def list_deal_documents(deal_id: str, db: Session = Depends(get_db)) -> list[DocumentRead]:
    if deal_service.get_deal(db, deal_id) is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return document_service.list_documents_for_deal(db, deal_id)


@router.post("/deals/{deal_id}/documents", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    deal_id: str,
    file: UploadFile = File(...),
    category: DocumentCategory = Form(...),
    db: Session = Depends(get_db),
) -> DocumentRead:
    if deal_service.get_deal(db, deal_id) is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    content = await file.read()
    max_size = settings.document_max_upload_size_mb * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size is {settings.document_max_upload_size_mb} MB.")
    try:
        return document_service.upload_document(db, deal_id, category, file.filename or "", content)
    except DocumentUploadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        logger.exception("Document upload failed for deal %s", deal_id)
        raise HTTPException(status_code=500, detail="Upload failed. Please try again.") from error
