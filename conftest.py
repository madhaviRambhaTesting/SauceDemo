"""
conftest.py — Pytest fixtures shared across the test suite.

Fixtures
--------
driver      : Launches the configured browser, navigates to BASE_URL,
              and quits the browser after each test function.
login_page  : Returns a fully initialised LoginPage bound to the active driver.
"""
import pytest
from utils.driver_factory import get_driver
from utils.config import BASE_URL
from utils.logger import get_logger
from pages.login_page import LoginPage

logger = get_logger("conftest")


@pytest.fixture(scope="function")
def driver():
    """Provide a browser driver instance for a single test function."""
    drv = get_driver()
    logger.info(f"Navigating to {BASE_URL}")
    drv.get(BASE_URL)
    yield drv
    drv.quit()
    logger.info("Browser closed.")


@pytest.fixture(scope="function")
def login_page(driver):
    """Return an initialised LoginPage object bound to the active driver."""
    return LoginPage(driver)
