"""
conftest.py — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript

Description : Root-level pytest configuration and shared fixtures.

Fixtures provided
-----------------
driver          — yields a configured WebDriver; auto-quits after the test.
login_page      — yields a LoginPage instance navigated to BASE_URL.
auto_screenshot — automatically captures a screenshot on test failure
                  and saves it to reports/screenshots/.
"""

import os
import logging
import pytest

from utils.driver_factory import DriverFactory
from utils.logger import TestLogger
from utils.config import SCREENSHOTS_DIR
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Session-scoped setup
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Called after command-line options have been parsed."""
    TestLogger.configure()


def pytest_sessionstart(session):
    """Ensure required output directories exist before any test runs."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    logger.info("pytest session started — screenshots dir: %s", SCREENSHOTS_DIR)


# ---------------------------------------------------------------------------
# Hooks — attach call-phase report to item for teardown use
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach run-phase result to the item so fixtures can inspect it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped WebDriver fixture.

    Yields
    ------
    selenium.webdriver.Remote
        A freshly created WebDriver for each test function.

    After the test
    --------------
    * Captures a screenshot if the test failed.
    * Calls ``driver.quit()`` unconditionally.
    """
    browser = request.config.getoption("--browser", default="chrome")
    _driver = DriverFactory.create_driver(browser)

    yield _driver

    # --- teardown ---
    _failed = (
        hasattr(request.node, "rep_call") and request.node.rep_call.failed
    )
    if _failed:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        safe = request.node.name.replace(" ", "_").replace("/", "_")
        path = os.path.join(SCREENSHOTS_DIR, f"{safe}_FAIL.png")
        try:
            _driver.save_screenshot(path)
            logger.info("📸 Auto-screenshot on failure: %s", path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Screenshot capture failed: %s", exc)

    _driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Return a ``LoginPage`` instance already navigated to BASE_URL.

    Depends on the ``driver`` fixture.
    """
    page = LoginPage(driver)
    page.load()
    logger.info("login_page fixture — page loaded at %s", driver.current_url)
    return page


@pytest.fixture(scope="function")
def auto_screenshot(request, driver):
    """
    Standalone screenshot fixture — attach to any test that needs explicit
    screenshot control.

    Yields the ``driver`` instance.  After the test, saves a screenshot
    named after the test if it failed.
    """
    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        safe = request.node.name.replace(" ", "_").replace("/", "_")
        path = os.path.join(SCREENSHOTS_DIR, f"{safe}_FAIL.png")
        try:
            driver.save_screenshot(path)
            logger.info("📸 auto_screenshot fixture saved: %s", path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("auto_screenshot: could not save — %s", exc)


# ---------------------------------------------------------------------------
# Custom CLI options
# ---------------------------------------------------------------------------

def pytest_addoption(parser):
    """Register custom command-line arguments."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests in: chrome (default) or firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (overrides config.py HEADLESS)",
    )
