# tests/test_tc83_login.py
"""
TC-83: Successful Login with Valid Username and Password
URL  : https://www.saucedemo.com/
Data : validdata.xlsx (standard_user / secret_sauce)
"""

import pytest
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import get_logger

logger = get_logger("TC-83")

# ── Test Data (from validdata.xlsx — row 1: standard_user / secret_sauce) ───
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"


class TestTC83SuccessfulLogin(BaseTest):
    """
    TC-83 — Successful Login with Valid Username and Password
    Linked Requirement: SAUC-3 — User Login with Username and Password
    Priority: High | Type: Manual (Automated via POM)
    """

    def test_step1_login_page_displayed(self):
        """Step 1: Navigate to the application login page and verify UI elements."""
        logger.info("TC-83 | Step 1: Verify login page is displayed.")
        login_page = LoginPage(self.driver)

        assert login_page.is_login_page_displayed(), (
            "FAIL: Login page elements (username, password, login-button) are NOT all visible."
        )
        logger.info("PASS: Login page displayed with all required fields.")

    def test_step2_enter_valid_username(self):
        """Step 2: Enter a valid registered username in the Username field."""
        logger.info(f"TC-83 | Step 2: Enter username '{VALID_USERNAME}'.")
        login_page = LoginPage(self.driver)
        login_page.enter_username(VALID_USERNAME)

        entered = login_page.get_attribute(
            *LoginPage.USERNAME_INPUT, "value"
        )
        assert entered == VALID_USERNAME, (
            f"FAIL: Expected username '{VALID_USERNAME}', got '{entered}'."
        )
        logger.info(f"PASS: Username '{VALID_USERNAME}' entered successfully.")

    def test_step3_enter_valid_password_and_verify_masking(self):
        """Step 3: Enter the valid password and verify it is masked."""
        logger.info("TC-83 | Step 3: Enter password and verify masking.")
        login_page = LoginPage(self.driver)
        login_page.enter_password(VALID_PASSWORD)

        assert login_page.is_password_masked(), (
            "FAIL: Password field is NOT masked (type != 'password')."
        )
        logger.info("PASS: Password entered and masked successfully.")

    def test_step4_click_login_redirects_to_dashboard(self):
        """Step 4: Full login flow — click Login and verify redirect to dashboard."""
        logger.info("TC-83 | Step 4: Full login and dashboard redirect verification.")
        login_page = LoginPage(self.driver)
        inventory_page = InventoryPage(self.driver)

        # Perform full login
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Assert redirect to inventory/dashboard
        assert inventory_page.is_on_inventory_page(), (
            f"FAIL: Expected URL to contain 'inventory.html', got '{self.driver.current_url}'."
        )
        assert inventory_page.is_dashboard_displayed(), (
            "FAIL: Dashboard/inventory container NOT visible after login."
        )
        logger.info(
            f"PASS: User redirected to dashboard — URL: {self.driver.current_url}"
        )

    def test_tc83_full_e2e_successful_login(self):
        """
        TC-83 — Full end-to-end test: Successful login with valid credentials.
        Combines all 4 steps in a single E2E flow.
        """
        logger.info("TC-83 | E2E: Starting full successful login test.")
        login_page = LoginPage(self.driver)
        inventory_page = InventoryPage(self.driver)

        # ── Step 1: Login page displayed ──────────────────────────────────
        assert login_page.is_login_page_displayed(), \
            "Step 1 FAIL: Login page elements not visible."
        logger.info("Step 1 PASS: Login page displayed.")

        # ── Step 2: Enter username ─────────────────────────────────────────
        login_page.enter_username(VALID_USERNAME)
        entered_user = login_page.get_attribute(*LoginPage.USERNAME_INPUT, "value")
        assert entered_user == VALID_USERNAME, \
            f"Step 2 FAIL: Username mismatch. Got '{entered_user}'."
        logger.info(f"Step 2 PASS: Username '{VALID_USERNAME}' entered.")

        # ── Step 3: Enter password (verify masking) ────────────────────────
        login_page.enter_password(VALID_PASSWORD)
        assert login_page.is_password_masked(), \
            "Step 3 FAIL: Password field not masked."
        logger.info("Step 3 PASS: Password masked and entered.")

        # ── Step 4: Click login & verify dashboard ─────────────────────────
        login_page.click_login()
        assert inventory_page.is_on_inventory_page(), \
            f"Step 4 FAIL: Not on inventory page. URL: {self.driver.current_url}"
        assert inventory_page.is_dashboard_displayed(), \
            "Step 4 FAIL: Dashboard container not visible."

        logger.info("Step 4 PASS: Redirected to dashboard successfully.")
        logger.info("TC-83 | E2E PASSED: Successful login verified end-to-end.")
