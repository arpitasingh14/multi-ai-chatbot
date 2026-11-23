"""FastAPI Application Entry Point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.core.config import settings
from backend.core.logging import configure_logging, logger
from backend.core.exceptions import CompanionException, ValidationException, ResourceNotFoundException
from backend.database.session import init_db
from backend.api.v1.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and teardown lifecycle events."""
    configure_logging()
    logger.info(f"Starting {settings.APP_NAME} in [{settings.APP_ENV}] mode...")

    # Initialize database tables on startup
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-oriented MVP of a Secure Multimodal AI Companion with RAG and Safety Guardrails",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
origins = settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, list) else [settings.ALLOWED_ORIGINS]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "validation_error", "message": exc.message, "details": exc.details},
    )


@app.exception_handler(ResourceNotFoundException)
async def not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "not_found", "message": exc.message},
    )


@app.exception_handler(CompanionException)
async def companion_exception_handler(request: Request, exc: CompanionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_error", "message": exc.message},
    )


# Register Routers
app.include_router(health_router, prefix=settings.API_V1_STR)


@app.get("/")
def root_redirect():
    """Root endpoint welcoming the caller and referencing docs."""
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
