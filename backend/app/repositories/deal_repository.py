from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.deal import Deal


class DealRepository:
    def list(self, db: Session) -> list[Deal]:
        return list(db.scalars(select(Deal).order_by(Deal.created_at)))

    def get_by_id(self, db: Session, deal_id: str) -> Deal | None:
        return db.get(Deal, deal_id)

    def create(self, db: Session, deal: Deal) -> Deal:
        db.add(deal)
        db.commit()
        db.refresh(deal)
        return deal
