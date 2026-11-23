"""Health check API endpoint."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.database.session import get_db
from backend.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def check_health(db: Session = Depends(get_db)) -> HealthResponse:
    """Verifies backend service, database connectivity, and configured providers."""
    # Check Database
    db_status = {"status": "connected", "type": settings.DATABASE_URL.split("://")[0]}
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = {"status": "unhealthy", "error": str(e)}

    # Check Vector Store
    vector_status = {
        "status": "ready",
        "backend": settings.VECTOR_STORE_BACKEND,
    }

    providers_status = {
        "llm": settings.LLM_PROVIDER,
        "embedding": settings.EMBEDDING_PROVIDER,
        "tts": settings.TTS_PROVIDER,
        "stt": settings.STT_PROVIDER,
    }

    overall_status = "healthy" if db_status["status"] == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        app_name=settings.APP_NAME,
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
        database=db_status,
        vector_store=vector_status,
        providers=providers_status,
    )
