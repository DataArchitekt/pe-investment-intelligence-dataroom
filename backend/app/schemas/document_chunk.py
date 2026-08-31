from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentChunkRead(BaseModel):
    chunk_id: str
    document_id: str
    deal_id: str
    chunk_text: str
    page_number: int | None
    section: str | None
    chunk_index: int
    token_count: int
    char_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
