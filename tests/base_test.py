"""
Base Test Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript

Description : Provides ``BaseTest`` — a pytest-compatible base class that
              handles WebDriver lifecycle (setup / teardown) and automatic
              screenshot capture on test failure.  All test classes should
              inherit from this rather than duplicating driver boilerplate.
"""

import os
import logging
import pytest

from utils.driver_factory import DriverFactory
from utils.config import SCREENSHOTS_DIR
from utils.logger import TestLogger

logger = logging.getLogger(__name__)


class BaseTest:
    """
    Pytest base class — sets up / tears down the WebDriver and captures a
    screenshot whenever a test fails.

    Usage
    -----
    .. code-block:: python

        class TestMyFeature(BaseTest):
            def test_something(self, driver):
                ...
    """

    # Injected by conftest.py fixture; stored here so teardown can access it
    driver = None

    @pytest.fixture(autouse=True)
    def setup_driver(self, request):
        """
        Pytest fixture: initialise the WebDriver before each test and quit
        it after, regardless of pass/fail outcome.

        The ``driver`` attribute is set on ``self`` so individual test methods
        can use ``self.driver`` if needed (in addition to the injected fixture).
        """
        TestLogger.configure()
        logger.info("=" * 70)
        logger.info("TEST START — %s", request.node.name)
        logger.info("=" * 70)

        self.driver = DriverFactory.create_driver()

        yield self.driver  # hand control to the test

        # ---- teardown ----
        if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
            self._capture_failure_screenshot(request.node.name)

        logger.info("=" * 70)
        logger.info("TEST END   — %s", request.node.name)
        logger.info("=" * 70)
        self.driver.quit()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _capture_failure_screenshot(self, test_name: str) -> None:
        """Save a screenshot when a test fails."""
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        safe_name = test_name.replace(" ", "_").replace("/", "_")
        filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_FAIL.png")
        try:
            self.driver.save_screenshot(filepath)
            logger.info("📸 Failure screenshot saved: %s", filepath)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not save screenshot: %s", exc)


# ---------------------------------------------------------------------------
# Pytest hook — used by BaseTest to detect failure in teardown
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach the call-phase report to the test item for teardown access."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
