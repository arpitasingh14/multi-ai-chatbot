"""Message ORM entity supporting text and multimodal conversation items."""

import uuid
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.conversation import Conversation


class Message(Base, TimestampMixin):
    """Represents an individual message exchanged in a conversation."""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    conversation_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,  # user, assistant, system
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    modality: Mapped[str] = mapped_column(
        String(50),
        default="text",  # text, image, audio, rag
        nullable=False,
    )
    message_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    # Relationship back to conversation
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
