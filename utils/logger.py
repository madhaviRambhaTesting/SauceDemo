"""
utils/logger.py — Centralised logger factory.

Usage
-----
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("message")
"""
import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger with a StreamHandler attached.

    Idempotent — calling get_logger with the same name twice will not
    duplicate handlers.

    Parameters
    ----------
    name : str
        Logical name for the logger (typically ``__name__``).

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
