# utils/logger.py

import logging
import os
from datetime import datetime


def get_logger(name: str = "pytest_script") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, "test_run.log"), encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
