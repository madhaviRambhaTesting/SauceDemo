"""
conftest.py
-----------
Pytest fixtures for the entire test suite.
The `driver` fixture is session-scoped per test function (function scope)
to ensure clean browser state between tests.
"""

import pytest
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


@pytest.fixture(scope="function")
def driver():
    """
    Provide a WebDriver instance for each test function.

    Yields the driver to the test; quits it after the test completes
    regardless of pass/fail outcome.
    """
    logger.info(
        f"[conftest] Initialising '{Config.BROWSER}' driver "
        f"(headless={Config.HEADLESS})"
    )
    web_driver = DriverFactory.get_driver(
        browser=Config.BROWSER,
        headless=Config.HEADLESS,
    )
    yield web_driver
    logger.info("[conftest] Quitting WebDriver")
    web_driver.quit()
