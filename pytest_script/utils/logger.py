"""
logger.py
---------
Logger — structured, colour-friendly logging helper.
Interface Segregation: a single focused utility with no external coupling.
"""

import logging
import sys


class Logger:
    """Factory for consistently configured Python loggers."""

    _FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Return a named logger with a StreamHandler attached.

        If the logger already has handlers (e.g., called twice with the
        same name), they are reused to avoid duplicate log lines.

        Parameters
        ----------
        name : str
            Logger name, typically ``__name__`` of the calling module.
        level : int
            Logging level (default: ``logging.INFO``).

        Returns
        -------
        logging.Logger
        """
        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(level)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter(
                fmt=Logger._FORMAT,
                datefmt=Logger._DATE_FORMAT,
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False

        return logger
