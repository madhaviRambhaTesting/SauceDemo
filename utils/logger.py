"""
Logger Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript

Description : Centralised logging configuration.  Call
              ``TestLogger.configure()`` once (from ``BaseTest.setup_driver``
              or ``conftest.py``) to set up both console and rotating-file
              handlers for the entire test run.
"""

import os
import logging
import logging.handlers
from utils.config import LOG_LEVEL, LOG_FILE, LOG_DIR


class TestLogger:
    """
    Utility class for configuring the Python logging subsystem.

    Only the first call to ``configure()`` has any effect; subsequent calls
    are no-ops (idempotent).
    """

    _configured: bool = False

    @classmethod
    def configure(cls, level: str | None = None) -> None:
        """
        Set up root logger with console + rotating-file handlers.

        Parameters
        ----------
        level : str, optional
            Override the log level (e.g. ``'DEBUG'``).  Defaults to the
            ``LOG_LEVEL`` config value.
        """
        if cls._configured:
            return

        os.makedirs(LOG_DIR, exist_ok=True)

        resolved_level = getattr(logging, (level or LOG_LEVEL).upper(), logging.INFO)

        fmt = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)-35s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        root = logging.getLogger()
        root.setLevel(resolved_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(resolved_level)
        console_handler.setFormatter(fmt)
        root.addHandler(console_handler)

        # Rotating file handler (5 MB × 3 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(resolved_level)
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)

        # Silence noisy third-party loggers
        for noisy in ("selenium", "urllib3", "webdriver_manager"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

        cls._configured = True
        logging.getLogger(__name__).info(
            "TestLogger configured — level=%s | logfile=%s",
            logging.getLevelName(resolved_level), LOG_FILE,
        )

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Return a named child logger (convenience wrapper)."""
        return logging.getLogger(name)
