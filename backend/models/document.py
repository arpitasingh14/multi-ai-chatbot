"""Document and DocumentChunk ORM models for RAG knowledge ingestion."""

import uuid
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Text, Integer, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    """Represents an uploaded document ingested into the RAG pipeline."""

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    file_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    processing_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",  # pending, processing, indexed, failed
        nullable=False,
        index=True,
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentChunk.chunk_index",
    )


class DocumentChunk(Base, TimestampMixin):
    """Represents a segmented text chunk from a document, indexed in the vector store."""

    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    page_number: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    vector_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    chunk_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="chunks",
    )
