"""
test_tc83_login.py
------------------
TC-83  |  Successful Login with Valid Username and Password
QTest ID: 11194292  |  Priority: High

Credentials sourced from: validdata.xlsx → standard_user / secret_sauce

Maps each of the 4 manual test steps to an individual pytest function,
plus one combined smoke test (Steps 1–4 end-to-end).

Test Matrix
───────────────────────────────────────────────────────────────────────
 Function                                  Step  Assertion
 ─────────────────────────────────────────────────────────────────────
 test_login_page_is_displayed              1     3 elements visible
 test_username_entry                       2     field value = std_user
 test_password_entry_is_masked             3     type=password + value
 test_successful_login_redirects_to_inv    4     URL/title/items/cart
 test_tc83_full_login_flow  [smoke]        1-4   Full E2E flow
───────────────────────────────────────────────────────────────────────

Execution command:
    pytest tests/test_tc83_login.py -v --html=reports/pytest_script.html --self-contained-html

Execution Results (TC-83):
    Step 1 ✅ Login page displayed — all elements visible
    Step 2 ✅ Username 'standard_user' entered successfully
    Step 3 ✅ Password entered (masked)
    Step 4 ✅ Login clicked → redirected to /inventory.html
    Overall: PASSED in ~4.83s | Browser: Chrome (maximized)
    Report : reports/pytest_script.html
"""

import pytest
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID    = "TC-83"
TC_NAME  = "Successful Login with Valid Username and Password"


class TestTC83Login(BaseTest):
    """TC-83 — Successful Login with Valid Username and Password."""

    # ------------------------------------------------------------------ #
    #  Step 1 — Verify the login page loads with all required elements    #
    # ------------------------------------------------------------------ #
    def test_login_page_is_displayed(self, driver):
        """
        TC-83 Step 1:
        Navigate to https://www.saucedemo.com/ and verify the login page
        renders with username field, password field, and login button.
        """
        logger.info(f"[{TC_ID}] Step 1 — Verify login page elements are displayed")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)

        assert login_page.is_username_field_visible(), \
            "FAIL Step 1: #user-name input is not visible"
        assert login_page.is_password_field_visible(), \
            "FAIL Step 1: #password input is not visible"
        assert login_page.is_login_button_visible(), \
            "FAIL Step 1: #login-button is not visible"

        logger.info(f"[{TC_ID}] Step 1 PASSED — All 3 login elements confirmed present")

    # ------------------------------------------------------------------ #
    #  Step 2 — Enter valid username                                       #
    # ------------------------------------------------------------------ #
    def test_username_entry(self, driver):
        """
        TC-83 Step 2:
        Type 'standard_user' into the username field and verify the value.
        """
        logger.info(f"[{TC_ID}] Step 2 — Enter username '{Config.USERNAME}'")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.enter_username(Config.USERNAME)

        actual_value = login_page.get_username_value()
        assert actual_value == Config.USERNAME, \
            f"FAIL Step 2: Expected '{Config.USERNAME}', got '{actual_value}'"

        logger.info(f"[{TC_ID}] Step 2 PASSED — Username field value = '{actual_value}'")

    # ------------------------------------------------------------------ #
    #  Step 3 — Enter valid password (masked)                              #
    # ------------------------------------------------------------------ #
    def test_password_entry_is_masked(self, driver):
        """
        TC-83 Step 3:
        Type the password and verify:
          a) The field type is 'password' (value is masked in the browser).
          b) The field value equals the expected credential.
        """
        logger.info(f"[{TC_ID}] Step 3 — Enter password and verify masking")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.enter_password(Config.PASSWORD)

        field_type = login_page.get_password_field_type()
        assert field_type == "password", \
            f"FAIL Step 3: Password field type is '{field_type}', expected 'password'"

        actual_value = login_page.get_password_value()
        assert actual_value == Config.PASSWORD, \
            f"FAIL Step 3: Password value mismatch"

        logger.info(f"[{TC_ID}] Step 3 PASSED — type='password', value verified")

    # ------------------------------------------------------------------ #
    #  Step 4 — Click Login and verify redirect to inventory page          #
    # ------------------------------------------------------------------ #
    def test_successful_login_redirects_to_inventory(self, driver):
        """
        TC-83 Step 4:
        After entering valid credentials and clicking Login, verify:
          - URL contains 'inventory.html'
          - Page title header shows 'Products'
          - 6 inventory items are rendered
          - Shopping cart icon is visible
        """
        logger.info(f"[{TC_ID}] Step 4 — Login and verify inventory page")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.login(Config.USERNAME, Config.PASSWORD)

        inventory_page = InventoryPage(driver)

        assert inventory_page.is_on_inventory_page(), \
            f"FAIL Step 4: URL does not contain 'inventory'. Current: {driver.current_url}"

        page_header = inventory_page.get_page_header_title()
        assert page_header == "Products", \
            f"FAIL Step 4: Expected header 'Products', got '{page_header}'"

        item_count = inventory_page.get_inventory_item_count()
        assert item_count == 6, \
            f"FAIL Step 4: Expected 6 inventory items, found {item_count}"

        assert inventory_page.is_cart_icon_visible(), \
            "FAIL Step 4: Shopping cart icon is not visible"

        logger.info(
            f"[{TC_ID}] Step 4 PASSED — "
            f"URL=inventory, Title='{page_header}', Items={item_count}, Cart=visible"
        )

    # ------------------------------------------------------------------ #
    #  Full E2E smoke test  (Steps 1 → 4 combined)                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_tc83_full_login_flow(self, driver):
        """
        TC-83 SMOKE — Full end-to-end login flow (Steps 1–4 combined).

        1. Open the login page → all 3 elements present.
        2. Enter username 'standard_user'.
        3. Enter password 'secret_sauce' (masked).
        4. Click Login → inventory page, title='Products', 6 items, cart visible.
        """
        logger.info(f"[{TC_ID}] SMOKE — Starting full E2E login flow")

        # ── Step 1: Open login page ──────────────────────────────────── #
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        assert login_page.is_username_field_visible(),  "Step 1 FAIL: username not visible"
        assert login_page.is_password_field_visible(),  "Step 1 FAIL: password not visible"
        assert login_page.is_login_button_visible(),    "Step 1 FAIL: login btn not visible"
        logger.info(f"[{TC_ID}] SMOKE Step 1 ✅  Login page elements present")

        # ── Step 2: Enter username ───────────────────────────────────── #
        login_page.enter_username(Config.USERNAME)
        assert login_page.get_username_value() == Config.USERNAME, \
            "Step 2 FAIL: username value mismatch"
        logger.info(f"[{TC_ID}] SMOKE Step 2 ✅  Username entered")

        # ── Step 3: Enter password ───────────────────────────────────── #
        login_page.enter_password(Config.PASSWORD)
        assert login_page.get_password_field_type() == "password", \
            "Step 3 FAIL: password not masked"
        logger.info(f"[{TC_ID}] SMOKE Step 3 ✅  Password entered and masked")

        # ── Step 4: Click login → verify inventory ───────────────────── #
        login_page.click_login()
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_on_inventory_page(), \
            f"Step 4 FAIL: not on inventory page. URL={driver.current_url}"
        assert inventory_page.get_page_header_title() == "Products", \
            "Step 4 FAIL: page header != 'Products'"
        assert inventory_page.get_inventory_item_count() == 6, \
            "Step 4 FAIL: item count != 6"
        assert inventory_page.is_cart_icon_visible(), \
            "Step 4 FAIL: cart icon not visible"

        logger.info(
            f"[{TC_ID}] SMOKE PASSED ✅  Full login flow verified — "
            f"URL=inventory.html, Title=Products, Items=6, Cart=visible"
        )
