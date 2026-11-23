"""Frontend configuration and environment variables."""

import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1")
APP_TITLE = "Secure Multimodal AI Companion"
APP_ICON = "🛡️"
APP_SUBTITLE = "Empathetic, Multimodal, and Grounded AI Assistant with Built-in Safety Guardrails"
