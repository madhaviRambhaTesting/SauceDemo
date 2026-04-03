# conftest.py

import pytest
import os
from utils.config import REPORT_DIR


def pytest_configure(config):
    """Ensure report directory exists before test run."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach outcome to node for screenshot-on-failure in BaseTest."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
