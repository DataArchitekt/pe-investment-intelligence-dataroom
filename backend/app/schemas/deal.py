from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DealCreate(BaseModel):
    deal_id: str
    name: str
    company_name: str
    industry: str
    geography: str
    revenue: Decimal
    ebitda: Decimal
    deal_stage: str


class DealRead(DealCreate):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
