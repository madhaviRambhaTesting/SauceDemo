# tests/test_login_page.py

import pytest
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import Config
from utils.logger import get_logger

logger = get_logger("TestLoginPage")


class TestLoginPage(BaseTest):
    """
    Test suite for TC-83: Successful Login with Valid Username and Password.

    Linked to: SAUC-3 - User Login with Username and Password
    Priority : High
    Status   : New
    """

    # ─────────────────────────────────────────────────────────────────────────
    # TC-83 | Successful Login with Valid Username and Password
    # ─────────────────────────────────────────────────────────────────────────

    @pytest.mark.tc83
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc83_login_page_is_displayed(self):
        """
        TC-83 | Step 1:
        Verify the login page is displayed with Username, Password fields
        and the Login button.
        """
        logger.info("TC-83 | Step 1 — Verifying Login page is displayed.")
        login_page = LoginPage(self.driver)

        assert login_page.is_login_page_displayed(), (
            "Login page was not displayed correctly. "
            "Expected: Username field, Password field, and Login button to be visible."
        )
        logger.info("TC-83 | Step 1 PASSED — Login page displayed correctly.")

    @pytest.mark.tc83
    @pytest.mark.smoke
    def test_tc83_enter_valid_username(self):
        """
        TC-83 | Step 2:
        Enter a valid registered username in the Username field.
        Verify username is entered successfully.
        """
        logger.info("TC-83 | Step 2 — Entering valid username.")
        login_page = LoginPage(self.driver)

        login_page.enter_username(Config.VALID_USERNAME)
        entered_value = login_page.get_attribute(LoginPage.USERNAME_FIELD, "value")

        assert entered_value == Config.VALID_USERNAME, (
            f"Expected username '{Config.VALID_USERNAME}', "
            f"but got '{entered_value}'."
        )
        logger.info(
            f"TC-83 | Step 2 PASSED — Username '{Config.VALID_USERNAME}' entered."
        )

    @pytest.mark.tc83
    @pytest.mark.smoke
    def test_tc83_enter_valid_password_masked(self):
        """
        TC-83 | Step 3:
        Enter the valid password. Verify password is masked (type='password')
        and entered successfully.
        """
        logger.info("TC-83 | Step 3 — Entering valid password and verifying masking.")
        login_page = LoginPage(self.driver)

        login_page.enter_password(Config.VALID_PASSWORD)
        field_type  = login_page.get_password_field_type()
        field_value = login_page.get_attribute(LoginPage.PASSWORD_FIELD, "value")

        assert field_type == "password", (
            f"Expected password field type 'password', got '{field_type}'."
        )
        assert field_value == Config.VALID_PASSWORD, (
            f"Expected password value to be set, got '{field_value}'."
        )
        logger.info("TC-83 | Step 3 PASSED — Password is masked and entered.")

    @pytest.mark.tc83
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc83_successful_login_redirects_to_dashboard(self):
        """
        TC-83 | Step 4 (End-to-End):
        Enter valid credentials → Click Login → Verify redirection to dashboard.
        Expected: User is redirected to /inventory.html successfully.
        """
        logger.info("TC-83 | Step 4 — Full login flow and dashboard redirection.")
        login_page     = LoginPage(self.driver)
        inventory_page = InventoryPage(self.driver)

        # Perform full login
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

        # Assert redirection to inventory/dashboard
        inventory_page.assert_on_inventory_page()
        assert inventory_page.is_dashboard_displayed(), (
            "Dashboard was not displayed after login. "
            "Expected: Inventory list and App logo to be visible."
        )

        logo_text = inventory_page.get_app_logo_text()
        assert logo_text == "Swag Labs", (
            f"Expected logo text 'Swag Labs', got '{logo_text}'."
        )

        logger.info(
            "TC-83 | Step 4 PASSED — Login successful. Redirected to dashboard."
        )
        logger.info(f"Current URL: {inventory_page.get_current_url()}")
