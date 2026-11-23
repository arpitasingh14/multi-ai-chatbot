"""Configuration settings loaded from environment variables using Pydantic Settings."""

import os
from pathlib import Path
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Central application configuration with strict validation."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    APP_NAME: str = "Secure Multimodal AI Companion"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    API_V1_STR: str = "/api/v1"

    # Security & CORS
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost:8501,http://127.0.0.1:8501"
    MAX_UPLOAD_SIZE_MB: int = 15

    # Database
    DATABASE_URL: str = "sqlite:///./storage/companion.db"

    # AI Model Providers
    LLM_PROVIDER: str = "mock"  # "gemini" | "openai" | "mock"
    EMBEDDING_PROVIDER: str = "mock"  # "gemini" | "openai" | "mock"
    LLM_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "text-embedding-004"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2048

    # API Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Vector Store Backend
    VECTOR_STORE_BACKEND: str = "memory"  # "chroma" | "memory"
    CHROMA_PERSIST_DIRECTORY: str = "./storage/vector_db"

    # RAG Tuning Parameters
    RAG_CHUNK_SIZE: int = 600
    RAG_CHUNK_OVERLAP: int = 80
    RAG_TOP_K: int = 4
    RAG_SIMILARITY_THRESHOLD: float = 0.65

    # Audio & Multimodal
    TTS_PROVIDER: str = "edge_tts"  # "edge_tts" | "pyttsx3" | "mock"
    TTS_VOICE: str = "en-US-AriaNeural"
    STT_PROVIDER: str = "mock"  # "whisper" | "mock"

    # Storage Paths
    UPLOAD_DIR: str = "./storage/uploads"
    PROCESSED_DIR: str = "./storage/processed"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


settings = Settings()
