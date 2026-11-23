"""Conversation ORM entity for session management."""

import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.message import Message
    from backend.models.safety_event import SafetyEvent


class Conversation(Base, TimestampMixin):
    """Represents a conversational session containing multiple messages."""

    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        default="New Conversation",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",  # active, archived, deleted
        nullable=False,
        index=True,
    )

    # Relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    safety_events: Mapped[List["SafetyEvent"]] = relationship(
        "SafetyEvent",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
