from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DocumentCategory(str, Enum):
    FINANCIAL = "Financial"
    COMMERCIAL = "Commercial"
    LEGAL = "Legal"
    HR = "HR"
    OPERATIONS = "Operations"
    CONTRACTS = "Contracts"
    CORPORATE = "Corporate"
    OTHER = "Other"


class DocumentStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    PROCESSED = "Processed"
    FAILED = "Failed"


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.deal_id"), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[DocumentCategory] = mapped_column(SqlEnum(DocumentCategory), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(SqlEnum(DocumentStatus), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(255), default="application/octet-stream", nullable=False
    )
    original_file_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    deal: Mapped["Deal"] = relationship(back_populates="documents")
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan", order_by="DocumentChunk.chunk_index"
    )

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)
