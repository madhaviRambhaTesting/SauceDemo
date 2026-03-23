"""
logger.py
---------
TC-83 | Successful Login with Valid Username and Password
Logger — structured logging helper with console output.
SOLID: Interface Segregation — a single-purpose utility with no external coupling.
       Single Responsibility — only manages logger creation and configuration.
"""

import logging
import sys
import os


class Logger:
    """
    Factory for consistently configured Python loggers.
    TC-83: Provides uniform log format across all POM classes and test files.
    """

    _FORMAT      = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Return a named logger with a StreamHandler (console) attached.

        Reuses existing handlers to prevent duplicate log lines if called
        multiple times with the same module name.

        Parameters
        ----------
        name : str
            Logger name, typically ``__name__`` of the calling module.
        level : int
            Logging level (default: ``logging.INFO``).

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(level)

            # Console handler (stdout — captured per-test by pytest)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            formatter = logging.Formatter(
                fmt=Logger._FORMAT,
                datefmt=Logger._DATE_FORMAT,
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # File handler (logs/ directory — persisted between runs)
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "tc83_test_run.log")
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.propagate = False

        return logger
