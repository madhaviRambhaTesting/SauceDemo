"""
Test Module  : TC-96 — Forgot Password Link is Visible on the Login Page
Repository   : madhaviRambhaTesting/SauceDemo
Branch       : qtestidscript
QTest ID     : 11194308
Priority     : HIGH 🔴
URL Under Test: https://www.saucedemo.com/

Description
-----------
Verifies that a 'Forgot Password' link (or equivalent password-reset element)
is present and visible on the SauceDemo login page.

Test Result (documented)
------------------------
❌ FAIL — saucedemo.com does NOT implement a 'Forgot Password' feature.
The login page DOM contains only:
  • #user-name  (Username input)
  • #password   (Password input)
  • #login-button (Submit button)
No anchor tag, button, or any element related to password recovery exists.

Execution Steps
---------------
1. Navigate to https://www.saucedemo.com/
2. Verify the login page is fully loaded (title, inputs, button)
3. Assert that 'Forgot Password' link is visible → FAILS (expected)
4. (Conditional) Click the link → SKIPPED due to step-3 failure
5. Verify navigation to password-reset page → SKIPPED

Screenshot
----------
Captured automatically on failure:
  reports/screenshots/TC96_forgot_password_FAIL.png
"""

import os
import logging
import pytest

from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.config import BASE_URL, SCREENSHOTS_DIR
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCREENSHOT_NAME = "TC96_forgot_password_FAIL.png"
TC_ID           = "TC-96"
QTEST_ID        = "11194308"


@pytest.mark.tc96
@pytest.mark.forgot_password
@pytest.mark.high_priority
class TestForgotPasswordLink(BaseTest):
    """
    Test class for TC-96.

    Inherits driver lifecycle management and automatic screenshot-on-failure
    from ``BaseTest``.
    """

    # ------------------------------------------------------------------
    # TC-96 Main Test
    # ------------------------------------------------------------------

    def test_forgot_password_link_visible(self, setup_driver):
        """
        TC-96 | QTest: 11194308
        Verify that the 'Forgot Password' link is visible on the login page.

        Steps
        -----
        1. Navigate to BASE_URL (https://www.saucedemo.com/)
        2. Confirm login page is loaded (title + key elements)
        3. Assert 'Forgot Password' link is visible
        4. Click the link (conditional on step 3)
        5. Assert navigation to a password-reset page

        Expected Result
        ---------------
        'Forgot Password' link is clearly visible → the test FAILS because
        the feature does not exist on saucedemo.com.
        """
        driver = setup_driver
        login_page = LoginPage(driver)

        # ---- Step 1: Navigate ----------------------------------------
        logger.info("[%s] Step 1 — Navigate to %s", TC_ID, BASE_URL)
        login_page.load()

        # ---- Step 2: Verify page loaded --------------------------------
        logger.info("[%s] Step 2 — Verify login page is loaded", TC_ID)
        assert login_page.is_loaded(), (
            f"[{TC_ID}] Login page did not load correctly. "
            f"Title='{driver.title}', URL='{driver.current_url}'"
        )
        logger.info(
            "[%s] ✅ Login page loaded — Title: '%s' | URL: %s",
            TC_ID, driver.title, driver.current_url,
        )

        # ---- Step 3: Assert 'Forgot Password' visible ------------------
        logger.info("[%s] Step 3 — Check 'Forgot Password' link visibility", TC_ID)

        forgot_visible = login_page.is_forgot_password_visible()

        if not forgot_visible:
            # Capture screenshot before asserting so it exists regardless
            _save_failure_screenshot(driver)

        assert forgot_visible is True, (
            f"[{TC_ID}] FAIL — 'Forgot Password' link should be visible on the "
            f"login page ({BASE_URL}), but it was NOT found in the DOM. "
            f"The SauceDemo application does not implement a password-reset feature. "
            f"QTest ID: {QTEST_ID}"
        )

        # ---- Step 4: Click the link (only reached if step 3 passes) ----
        logger.info("[%s] Step 4 — Click 'Forgot Password' link", TC_ID)
        try:
            login_page.click_forgot_password()
            logger.info("[%s] ✅ 'Forgot Password' link clicked successfully", TC_ID)
        except NoSuchElementException as exc:
            pytest.skip(
                f"[{TC_ID}] Step 4 SKIPPED — Cannot click 'Forgot Password': {exc}"
            )

        # ---- Step 5: Verify navigation ---------------------------------
        logger.info("[%s] Step 5 — Verify navigation to password-reset page", TC_ID)
        current_url = driver.current_url
        assert "forgot" in current_url.lower() or "reset" in current_url.lower(), (
            f"[{TC_ID}] Expected URL to contain 'forgot' or 'reset' after clicking "
            f"the link, but got: {current_url}"
        )
        logger.info("[%s] ✅ Navigated to reset page: %s", TC_ID, current_url)

    # ------------------------------------------------------------------
    # Additional negative / boundary tests
    # ------------------------------------------------------------------

    def test_login_page_elements_present(self, setup_driver):
        """
        Sanity check — confirm the standard login elements exist.
        This isolates the TC-96 failure: standard elements ARE present,
        only the 'Forgot Password' link is absent.
        """
        from selenium.webdriver.common.by import By

        driver = setup_driver
        login_page = LoginPage(driver)
        login_page.load()

        assert login_page.is_loaded(), (
            f"[{TC_ID}] Sanity — login page failed to load"
        )

        # Confirm exactly the three standard elements exist
        standard_elements = {
            "Username input" : (By.ID, "user-name"),
            "Password input" : (By.ID, "password"),
            "Login button"   : (By.ID, "login-button"),
        }
        for name, locator in standard_elements.items():
            assert login_page.is_element_visible(locator), (
                f"[{TC_ID}] Expected '{name}' to be visible but it was NOT found."
            )
            logger.info("[%s] ✅ '%s' is visible on login page", TC_ID, name)

        logger.info(
            "[%s] Sanity PASS — all 3 standard login elements are present. "
            "'Forgot Password' is the only missing element.",
            TC_ID,
        )

    def test_no_forgot_password_anchor_in_dom(self, setup_driver):
        """
        DOM-level confirmation that zero <a> tags related to 'Forgot Password'
        exist anywhere on the login page.
        """
        from selenium.webdriver.common.by import By

        driver = setup_driver
        login_page = LoginPage(driver)
        login_page.load()

        all_anchors = login_page.find_elements((By.TAG_NAME, "a"))
        forgot_anchors = [
            a for a in all_anchors
            if "forgot" in (a.get_attribute("href") or "").lower()
            or "forgot" in (a.text or "").lower()
        ]

        logger.info(
            "[%s] DOM anchor audit — total <a> tags: %d | "
            "forgot-related <a> tags: %d",
            TC_ID, len(all_anchors), len(forgot_anchors),
        )

        assert len(forgot_anchors) == 0, (
            f"[{TC_ID}] Unexpected: found {len(forgot_anchors)} 'Forgot Password' "
            f"anchor tag(s) — the application may have changed."
        )
        logger.info(
            "[%s] ✅ Confirmed — 0 'Forgot Password' anchor tags in DOM.", TC_ID
        )


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _save_failure_screenshot(driver) -> None:
    """Persist a failure screenshot to the reports/screenshots directory."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOTS_DIR, SCREENSHOT_NAME)
    try:
        driver.save_screenshot(filepath)
        logger.info("📸 Failure screenshot saved → %s", filepath)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not capture screenshot: %s", exc)
