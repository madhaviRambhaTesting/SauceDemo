# =============================================================================
# utils/logger.py
# -----------------------------------------------------------------------------
# Responsibility : Centralised logging configuration for the entire framework.
# Design         : Module-level singleton initialisation; call once in conftest.
# Compliance     : SRP — only concerned with log formatting and handler setup.
# =============================================================================

import logging
import sys
from pathlib import Path


def setup_logging(
    log_level: int = logging.DEBUG,
    log_file: str  = "reports/test_run.log",
) -> logging.Logger:
    """
    Configure root logger with console + rotating file handlers.

    Call this ONCE from conftest.py (session scope) so all modules share
    the same handlers without duplication.

    Args:
        log_level (int) : Minimum severity to capture (default: DEBUG).
        log_file  (str) : Relative path for the file handler output.

    Returns:
        logging.Logger: Configured root logger instance.
    """
    # ── Ensure the reports directory exists ──────────────────────────────────
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()

    # Guard: avoid adding duplicate handlers on repeated calls
    if root_logger.handlers:
        return root_logger

    root_logger.setLevel(log_level)

    fmt = logging.Formatter(
        fmt    = "%(asctime)s | %(levelname)-8s | %(name)-35s | %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler (stdout) ──────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(fmt)

    # ── File handler ──────────────────────────────────────────────────────────
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(fmt)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    root_logger.info("Logger initialised → level=%s | file=%s", log_level, log_file)
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Return a named child logger for a specific module/class.

    Args:
        name (str): Typically __name__ of the calling module.

    Returns:
        logging.Logger: Named logger that inherits root configuration.
    """
    return logging.getLogger(name)
