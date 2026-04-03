"""
logger.py
---------
Centralised logging utility for the test automation framework.
Follows SRP — only responsible for creating and returning configured loggers.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
"""

import logging
import os
from datetime import datetime


def get_logger(name: str = "TC96_Logger") -> logging.Logger:
    """
    Creates and returns a logger with both console and file handlers.

    Args:
        name (str): Name of the logger. Defaults to 'TC96_Logger'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Formatter ────────────────────────────────────────────────────────────
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console Handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ── File Handler ──────────────────────────────────────────────────────────
    log_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"tc96_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
