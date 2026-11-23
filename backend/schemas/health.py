"""Health check schema definition."""

from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """System health status response schema."""

    status: str = Field(..., description="Overall service status (healthy/degraded)")
    app_name: str = Field(..., description="Application name")
    version: str = Field("1.0.0", description="API version")
    timestamp: datetime = Field(..., description="Current server time (UTC)")
    database: Dict[str, Any] = Field(..., description="Database connectivity status")
    vector_store: Dict[str, Any] = Field(..., description="Vector store backend status")
    providers: Dict[str, str] = Field(..., description="Active configured providers")
