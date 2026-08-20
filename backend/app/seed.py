from sqlalchemy.orm import Session

from app.models.deal import Deal


def seed_database(db: Session) -> None:
    """Add the sample deal once, without overwriting user data."""
    if db.get(Deal, "ABC-HYD-001") is None:
        db.add(
            Deal(
                deal_id="ABC-HYD-001",
                name="ABC Hydraulic Systems",
                company_name="ABC Hydraulic Systems",
                industry="Industrial Manufacturing",
                geography="North America",
                revenue=120_000_000,
                ebitda=18_000_000,
                deal_stage="Due Diligence",
            )
        )
        db.commit()
