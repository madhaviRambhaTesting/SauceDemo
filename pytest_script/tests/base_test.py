# tests/base_test.py

import pytest
import os
from utils.driver_factory import DriverFactory
from utils.config import BASE_URL, BROWSER, HEADLESS
from utils.logger import get_logger

logger = get_logger("BaseTest")


class BaseTest:
    """Base test class — manages driver lifecycle and navigation."""

    driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self, request):
        """Setup: launch browser, maximize, navigate. Teardown: screenshot on fail, close browser."""
        logger.info(f"=== TEST START: {request.node.name} ===")
        self.driver = DriverFactory.get_driver(browser=BROWSER, headless=HEADLESS)
        self.driver.implicitly_wait(10)
        logger.info(f"Navigating to BASE_URL: {BASE_URL}")
        self.driver.get(BASE_URL)

        yield  # ── Test runs here ──

        # Teardown
        if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
            from pages.base_page import BasePage
            bp = BasePage(self.driver)
            screenshot_path = bp.take_screenshot(request.node.name)
            logger.error(f"TEST FAILED — Screenshot: {screenshot_path}")
            # Attach to pytest-html report
            if hasattr(request.config, "_html"):
                extras = getattr(request.node, "extras", [])
                import pytest_html
                extras.append(pytest_html.extras.image(screenshot_path))
                request.node.extras = extras

        if self.driver:
            logger.info(f"=== TEST END: {request.node.name} — Closing browser ===")
            self.driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcome for screenshot-on-failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
