"""Security utilities for filename sanitization, MIME verification, and input safety."""

import os
import re
from pathlib import Path
from typing import Set
from backend.core.exceptions import ValidationException

# Allowed file extensions
ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt", ".md", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".m4a"}
ALLOWED_DOCUMENT_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt", ".md"}
ALLOWED_IMAGE_EXTENSIONS: Set[str] = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_AUDIO_EXTENSIONS: Set[str] = {".wav", ".mp3", ".m4a"}


def sanitize_filename(filename: str) -> str:
    """Sanitizes user-provided filename to prevent path traversal and arbitrary file overwrite."""
    if not filename:
        raise ValidationException("Filename cannot be empty")

    clean_name = os.path.basename(filename)
    clean_name = clean_name.replace("\x00", "").replace("/", "").replace("\\", "")
    clean_name = re.sub(r"[^a-zA-Z0-9._-]", "_", clean_name)
    clean_name = clean_name.lstrip(".-")

    if not clean_name:
        clean_name = "unnamed_document"

    max_length = 200
    if len(clean_name) > max_length:
        stem, ext = os.path.splitext(clean_name)
        clean_name = stem[: max_length - len(ext)] + ext

    return clean_name


def validate_file_extension(filename: str, allowed: Set[str]) -> str:
    """Validates file extension against allowed set."""
    ext = Path(filename).suffix.lower()
    if ext not in allowed:
        raise ValidationException(
            f"Unsupported file format '{ext}'. Allowed formats: {', '.join(sorted(allowed))}"
        )
    return ext


def is_path_safe(base_dir: Path, target_path: Path) -> bool:
    """Verifies target path resides strictly inside base_dir, preventing directory traversal."""
    try:
        resolved_base = base_dir.resolve()
        resolved_target = target_path.resolve()
        return str(resolved_target).startswith(str(resolved_base))
    except (ValueError, RuntimeError):
        return False
