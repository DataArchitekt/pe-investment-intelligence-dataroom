from sqlalchemy.orm import Session

from app.models.deal import Deal
from app.repositories.deal_repository import DealRepository
from app.schemas.deal import DealCreate


class DealService:
    def __init__(self, repository: DealRepository | None = None) -> None:
        self.repository = repository or DealRepository()

    def list_deals(self, db: Session) -> list[Deal]:
        return self.repository.list(db)

    def get_deal(self, db: Session, deal_id: str) -> Deal | None:
        return self.repository.get_by_id(db, deal_id)

    def create_deal(self, db: Session, payload: DealCreate) -> Deal:
        return self.repository.create(db, Deal(**payload.model_dump()))
