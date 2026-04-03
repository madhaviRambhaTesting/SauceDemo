"""
base_test.py
------------
BaseTest class that all test classes inherit from.
Manages WebDriver setup and teardown, and provides auto-screenshot
capability on test failure.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from pages.base_page import BasePage


class BaseTest:
    """
    Base class for all test classes.
    Provides:
    - driver: Selenium WebDriver instance (setup/teardown per test method)
    - logger: Shared logger
    - auto_screenshot_on_failure: Captures screenshot when a test fails
    """

    driver: WebDriver = None
    logger = get_logger("BaseTest")

    @pytest.fixture(autouse=True)
    def setup_teardown(self, request):
        """
        Pytest fixture that runs before and after each test method.
        Opens a new Chrome browser instance before each test and
        quits it after, taking a screenshot if the test failed.
        """
        self.logger.info(
            f"{'='*60}\n  START: {request.node.name}\n{'='*60}"
        )

        # ── Setup ─────────────────────────────────────────────────────────────
        headless = request.config.getoption("--headless", default=False)
        self.driver = DriverFactory.get_driver(headless=bool(headless))

        yield  # ── Test runs here ─────────────────────────────────────────────

        # ── Teardown ──────────────────────────────────────────────────────────
        # Check if the test failed and capture a screenshot
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            self.logger.warning(
                f"Test FAILED: {request.node.name} — capturing screenshot."
            )
            page = BasePage(self.driver)
            page.take_screenshot(test_name=request.node.name, status="FAIL")

        if self.driver:
            self.driver.quit()
            self.logger.info(f"Driver closed after: {request.node.name}")

        self.logger.info(
            f"{'='*60}\n  END: {request.node.name}\n{'='*60}"
        )
