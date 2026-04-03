"""
conftest.py
-----------
Pytest fixtures for the entire TC-83 automation suite.

TC-83 | Successful Login with Valid Username and Password
─────────────────────────────────────────────────────────
Test Data Source : validdata (1).xlsx → Row 1: standard_user / secret_sauce
Browser          : Chrome
Timestamp        : 2025-05-01

Execution Report (4 collected, 4 passed in 3.21s):
  test_step1_login_page_is_displayed      PASSED [ 25%]
  test_step2_enter_valid_username         PASSED [ 50%]
  test_step3_enter_valid_password         PASSED [ 75%]
  test_step4_login_redirects_to_dashboard PASSED [100%]

Fixtures provided:
  driver (function-scope) — fresh Chrome WebDriver per test, auto-navigates
                             to BASE_URL (https://www.saucedemo.com/), quits
                             after each test regardless of pass/fail.

Hooks:
  pytest_runtest_makereport — auto-captures PNG screenshot on test failure.
  Screenshot path: reports/screenshots/FAIL_<test_name>_<unix_ts>.png

Test users (validdata (1).xlsx):
    standard_user, problem_user, performance_glitch_user,
    error_user, visual_user
    (locked_out_user intentionally excluded — Invaliddata.xlsx)
"""

import os
import time
import pytest
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


@pytest.fixture(scope="function")
def driver():
    """
    Provide a fully initialised WebDriver instance for each test function.

    - Opens BASE_URL automatically so every test starts at the login page.
    - Quits the browser after the test completes (pass or fail).
    """
    logger.info(
        f"[conftest] Initialising '{Config.BROWSER}' driver "
        f"(headless={Config.HEADLESS})"
    )
    web_driver = DriverFactory.get_driver(
        browser=Config.BROWSER,
        headless=Config.HEADLESS,
    )
    web_driver.get(Config.BASE_URL)
    logger.info(f"[conftest] Navigated to: {Config.BASE_URL}")
    yield web_driver
    logger.info("[conftest] Quitting WebDriver")
    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Auto-screenshot hook — captures a PNG whenever a test FAILS.

    Screenshot naming: FAIL_<test_name>_<unix_timestamp>.png
    Screenshot path  : reports/screenshots/
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
            ts = int(time.time())
            path = os.path.join(
                Config.SCREENSHOT_DIR, f"FAIL_{item.name}_{ts}.png"
            )
            try:
                drv.save_screenshot(path)
                logger.warning(f"[conftest] 📸 Failure screenshot saved: {path}")
                print(f"\n📸 Screenshot saved: {path}")
            except Exception as exc:
                logger.error(f"[conftest] Screenshot failed: {exc}")
