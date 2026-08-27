from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentCategory, DocumentStatus


class DocumentRead(BaseModel):
    document_id: str
    deal_id: str
    file_name: str
    category: DocumentCategory
    file_path: str
    status: DocumentStatus
    summary: str | None
    file_size: int
    content_type: str
    original_file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
