from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.deal import DealCreate, DealRead
from app.schemas.document import DocumentRead
from app.services.deal_service import DealService
from app.services.document_service import DocumentService

router = APIRouter(tags=["deals"])
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
