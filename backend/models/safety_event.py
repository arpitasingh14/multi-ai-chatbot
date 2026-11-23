"""Safety audit event entity tracking guardrail triggers without storing raw PII."""

import uuid
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.conversation import Conversation


class SafetyEvent(Base, TimestampMixin):
    """Represents a detected safety trigger, crisis flag, or prompt injection attempt."""

    __tablename__ = "safety_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    conversation_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,  # crisis_detected, prompt_injection, medical_refusal, toxic_input
        index=True,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,  # LOW, MEDIUM, HIGH, CRITICAL
        index=True,
    )
    action_taken: Mapped[str] = mapped_column(
        String(100),
        nullable=False,  # interrupted_and_helpline_shown, sanitized, rejected, logged
    )
    event_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    conversation: Mapped[Optional["Conversation"]] = relationship(
        "Conversation",
        back_populates="safety_events",
    )
