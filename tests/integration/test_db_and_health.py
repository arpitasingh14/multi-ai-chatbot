"""Integration tests for database session and health API endpoint."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.session import SessionLocal, init_db
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.models.document import Document
from backend.models.safety_event import SafetyEvent


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()
    yield


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"]["status"] == "connected"
    assert data["providers"]["llm"] == "mock"


def test_models_persisted_in_db():
    db = SessionLocal()
    try:
        # Create a conversation
        conv = Conversation(title="Test Phase 1 Conversation")
        db.add(conv)
        db.commit()
        db.refresh(conv)
        assert conv.id is not None
        assert conv.title == "Test Phase 1 Conversation"

        # Create a message attached to conversation
        msg = Message(
            conversation_id=conv.id,
            role="user",
            content="Hello from test",
            modality="text",
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        assert msg.id is not None
        assert msg.conversation_id == conv.id

        # Verify relationship loading
        assert len(conv.messages) == 1
        assert conv.messages[0].content == "Hello from test"

        # Clean up
        db.delete(conv)
        db.commit()
    finally:
        db.close()
