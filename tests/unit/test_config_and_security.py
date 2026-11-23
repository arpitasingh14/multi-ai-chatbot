"""Unit tests for configuration loading and security utilities."""

import pytest
from pathlib import Path
from backend.core.config import settings
from backend.core.security import sanitize_filename, validate_file_extension, is_path_safe
from backend.core.exceptions import ValidationException


def test_settings_loaded():
    assert settings.APP_NAME == "Secure Multimodal AI Companion"
    assert settings.MAX_UPLOAD_SIZE_MB == 15
    assert settings.max_upload_size_bytes == 15 * 1024 * 1024
    assert isinstance(settings.ALLOWED_ORIGINS, list)


def test_sanitize_filename():
    assert sanitize_filename("normal_doc.pdf") == "normal_doc.pdf"
    assert sanitize_filename("../../../etc/passwd") == "passwd"
    assert sanitize_filename("..\\..\\windows\\system32\\calc.exe") == "calc.exe"
    assert sanitize_filename("my file with spaces.docx") == "my_file_with_spaces.docx"
    assert sanitize_filename("dangerous; rm -rf.txt") == "dangerous__rm_-rf.txt"


def test_validate_file_extension():
    allowed = {".pdf", ".docx", ".txt"}
    assert validate_file_extension("notes.pdf", allowed) == ".pdf"
    assert validate_file_extension("DOCUMENT.DOCX", allowed) == ".docx"

    with pytest.raises(ValidationException):
        validate_file_extension("script.exe", allowed)


def test_is_path_safe():
    base = Path("./storage/uploads").resolve()
    safe_child = base / "safe_file.txt"
    unsafe_escape = base / ".." / "secret.key"

    assert is_path_safe(base, safe_child) is True
    assert is_path_safe(base, unsafe_escape) is False
