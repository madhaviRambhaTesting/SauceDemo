"""
conftest.py
-----------
TC-83 | Successful Login with Valid Username and Password
Pytest session fixtures — shared across all TC-83 test functions.

Fixture scope: 'function' — fresh browser per test ensures:
  - Clean cookies / session state for every test
  - Isolation between TC-83 steps
  - No cross-test contamination
"""

import os
import pytest
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID = "TC-83"


def pytest_configure(config):
    """
    TC-83: Ensure reports/ and logs/ directories exist before any test runs.
    Called once at the start of the pytest session.
    """
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    logger.info(
        f"[{TC_ID}] [conftest] Session configured | "
        f"reports={Config.REPORT_DIR} | logs=logs/"
    )


@pytest.fixture(scope="function")
def driver():
    """
    TC-83 WebDriver fixture — function scope.

    Provides a fully configured browser instance for each test.
    Tears down (quits) the driver after every test regardless of outcome.

    Yields
    ------
    selenium.webdriver.Remote
        Active WebDriver instance pointed at Config.BASE_URL browser.
    """
    logger.info(
        f"[{TC_ID}] [conftest] ▶ Initialising '{Config.BROWSER}' driver "
        f"(headless={Config.HEADLESS}) for TC-83"
    )
    web_driver = DriverFactory.get_driver(
        browser=Config.BROWSER,
        headless=Config.HEADLESS,
    )
    yield web_driver
    logger.info(f"[{TC_ID}] [conftest] ■ Quitting WebDriver after test completion")
    web_driver.quit()
