"""Central logging configuration adhering to security guardrails.
Sensitive conversation contents and raw user inputs are excluded from logs.
"""

import logging
import sys
from backend.core.config import settings


def configure_logging() -> None:
    """Configures structured application logging."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Custom log format with timestamp, level, module, and message
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Reset root logger handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Silence excessively verbose external loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger("companion")
