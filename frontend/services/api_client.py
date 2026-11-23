"""HTTP Client for communicating with the FastAPI backend."""

import httpx
from typing import Dict, Any, Optional
from frontend.config import BACKEND_API_URL


class APIClient:
    """Synchronous/Asynchronous HTTP client for backend REST API."""

    def __init__(self, base_url: str = BACKEND_API_URL, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def check_health(self) -> Dict[str, Any]:
        """Calls GET /health to verify backend connectivity."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"status": "unreachable", "error": str(e)}


api_client = APIClient()
