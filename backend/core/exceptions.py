"""Custom application exceptions and centralized error handling models."""

from typing import Any, Optional


class CompanionException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationException(CompanionException):
    """Raised on invalid user input or malformed request payload."""
    pass


class SecurityException(CompanionException):
    """Raised when safety rules, rate limits, or access constraints are breached."""
    pass


class DocumentProcessingException(CompanionException):
    """Raised when document extraction, chunking, or indexing fails."""
    pass


class RAGException(CompanionException):
    """Raised when vector retrieval or context augmentation fails."""
    pass


class ProviderException(CompanionException):
    """Raised when external AI providers encounter an error."""
    pass


class ResourceNotFoundException(CompanionException):
    """Raised when a requested resource (conversation, document) is not found."""
    pass
