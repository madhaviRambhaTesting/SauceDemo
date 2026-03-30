"""
tests/test_tc83_login.py
========================
Test Case  : TC-83 — Successful Login with Valid Username and Password
Application: https://www.saucedemo.com/
Framework  : Selenium + Pytest + Page Object Model (SOLID-compliant)

Test Steps
----------
1. Navigate to the SauceDemo login page.
2. Verify the login page is fully displayed (username field, password field,
   Login button are all visible).
3. Enter valid username  → ``standard_user``
4. Enter valid password  → ``secret_sauce``
5. Click the **Login** button.
6. Assert redirection to the inventory/dashboard page
   (``/inventory.html`` present in URL and app logo visible).

Test Data
---------
Primary   : loaded from ``test_data/validdata.xlsx`` (row 2, columns B & C).
Fallback  : hard-coded ``standard_user / secret_sauce`` when the xlsx is absent.

Fixtures (from conftest.py)
---------------------------
driver     : browser session, scoped per function.
login_page : LoginPage POM instance bound to the active driver.
"""

import os

import openpyxl
import pytest

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("test_tc83_login")

# ── Test-data helpers ─────────────────────────────────────────────────────────

_EXCEL_PATH = os.path.join("test_data", "validdata.xlsx")
_FALLBACK_USERNAME = "standard_user"
_FALLBACK_PASSWORD = "secret_sauce"


def load_valid_credentials() -> tuple[str, str]:
    """
    Read the first data row from ``test_data/validdata.xlsx``.

    Expected sheet layout
    ---------------------
    Row 1  : header  (ignored)
    Row 2+ : data    — column B = username, column C = password

    Returns
    -------
    tuple[str, str]
        (username, password) for ``standard_user``.

    Raises
    ------
    FileNotFoundError
        When the workbook cannot be located (caller falls back to constants).
    IndexError
        When the sheet contains no data rows.
    """
    wb = openpyxl.load_workbook(_EXCEL_PATH)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))   # skip header
    username = str(rows[0][1])   # column B
    password = str(rows[0][2])   # column C
    return username, password


# ── TC-83 Test Class ──────────────────────────────────────────────────────────

class TestTC83SuccessfulLogin:
    """
    Automated test class for TC-83: Successful Login with Valid Credentials.

    Each test method maps to one or more documented test steps and uses the
    ``login_page`` fixture from conftest.py.
    """

    # ------------------------------------------------------------------
    # TC-83 — Step 1 (standalone smoke check)
    # ------------------------------------------------------------------

    def test_step1_login_page_is_displayed(self, login_page: LoginPage):
        """
        TC-83 | Step 1 — Login page must be displayed with all required elements.

        Asserts
        -------
        * Username input field is visible.
        * Password input field is visible.
        * Login button is visible.
        """
        logger.info("TC-83 | Step 1: Verifying login page elements are visible.")
        assert login_page.is_login_page_displayed(), (
            "TC-83 Step 1 FAILED: "
            "One or more login page elements (username, password, login-button) "
            "are not visible."
        )
        logger.info("TC-83 | Step 1: PASSED — Login page elements confirmed visible.")

    # ------------------------------------------------------------------
    # TC-83 — Full end-to-end flow (Steps 1 → 4)
    # ------------------------------------------------------------------

    def test_tc83_successful_login_with_valid_credentials(
        self, login_page: LoginPage, request
    ):
        """
        TC-83 — Full end-to-end login flow with valid credentials.

        Steps covered
        -------------
        1. Verify login page is displayed.
        2. Enter valid username.
        3. Enter valid password.
        4. Click Login → assert redirect to inventory dashboard.

        Expected result
        ---------------
        * URL contains ``inventory``.
        * App logo (dashboard header) is visible.
        """
        test_name: str = request.node.name
        logger.info(f"TC-83 | Starting full login flow: '{test_name}'")

        # ── Step 1: Login page displayed ─────────────────────────────────────
        logger.info("TC-83 | Step 1: Verify login page is displayed.")
        assert login_page.is_login_page_displayed(), (
            "TC-83 Step 1 FAILED: Login page not displayed correctly."
        )
        logger.info("TC-83 | Step 1: PASSED.")

        # ── Steps 2 & 3: Resolve credentials ─────────────────────────────────
        try:
            username, password = load_valid_credentials()
            logger.info(
                f"TC-83 | Credentials loaded from Excel: username='{username}'"
            )
        except Exception as exc:
            username, password = _FALLBACK_USERNAME, _FALLBACK_PASSWORD
            logger.warning(
                f"TC-83 | Excel not found ({exc}). "
                f"Using fallback credentials: username='{username}'"
            )

        # ── Step 2: Enter username ─────────────────────────────────────────────
        logger.info(f"TC-83 | Step 2: Entering username='{username}'.")
        login_page.enter_username(username)
        logger.info("TC-83 | Step 2: PASSED.")

        # ── Step 3: Enter password ─────────────────────────────────────────────
        logger.info("TC-83 | Step 3: Entering password (value masked in log).")
        login_page.enter_password(password)
        logger.info("TC-83 | Step 3: PASSED.")

        # ── Step 4: Click Login & assert dashboard ─────────────────────────────
        logger.info("TC-83 | Step 4: Clicking Login button.")
        login_page.click_login()

        # Capture screenshot immediately after login attempt (pass OR fail)
        screenshot_path = login_page.take_screenshot(test_name)
        logger.info(f"TC-83 | Screenshot saved: {screenshot_path}")

        # Assert 1 — dashboard / app logo is visible
        assert login_page.is_dashboard_displayed(), (
            "TC-83 Step 4 FAILED: "
            "Dashboard (app_logo) not visible after clicking Login."
        )

        # Assert 2 — URL confirms redirect to inventory page
        current_url: str = login_page.get_current_url()
        logger.info(f"TC-83 | Redirected to: {current_url}")
        assert "inventory" in current_url, (
            f"TC-83 Step 4 FAILED: "
            f"Expected 'inventory' in URL but got '{current_url}'."
        )

        logger.info(
            f"TC-83 | PASSED — Successful login verified. "
            f"Final URL: {current_url}"
        )
