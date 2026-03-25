# conftest.py — TC-83 | SauceDemo Login Automation Suite

import pytest
from utils.logger import get_logger

logger = get_logger("conftest")


def pytest_configure(config):
    """Register custom markers to avoid PytestUnknownMarkWarning."""
    config.addinivalue_line("markers", "tc83: TC-83 – Successful Login")
    config.addinivalue_line("markers", "smoke: Smoke test suite")
    config.addinivalue_line("markers", "regression: Regression test suite")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to expose test result to the setup fixture (for screenshot-on-fail logic).
    Attaches the test call report to the test node as 'rep_call'.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_html_report_title(report):
    """Sets the HTML report page title."""
    report.title = "TC-83 | Swag Labs – Login Test Report"
