"""
test_tc83_login.py
------------------
TC-83  |  Successful Login with Valid Username and Password
QTest ID : TC-83  |  Priority: High  |  Status: New
Linked   : SAUC-3 — User Login with Username and Password

Live Browser Execution Results:
  ✅ Step 1 | Navigate to https://www.saucedemo.com/        → Login page loaded
  ✅ Step 2 | Enter username 'standard_user'                → id=user-name confirmed
  ✅ Step 3 | Enter password 'secret_sauce'                 → type=password (masked)
  ✅ Step 4 | Click Login button                            → inventory.html ✔
  ✅ Assert | Page header == 'Products'                     ✔
  ✅ Assert | 6 inventory items loaded                      ✔
  ✅ Assert | No error banner                               ✔

Test Matrix
───────────────────────────────────────────────────────────────────────────────
 Function                                       Step   Assertion
 ────────────────────────────────────────────────────────────────────────────
 test_tc83_login_page_displayed                 1      3 elements visible
 test_tc83_enter_username                       2      field value = standard_user
 test_tc83_enter_password                       3      type=password + value masked
 test_tc83_successful_login_redirects_to_inv    4      URL/header/6items/cart
 test_tc83_login_no_error_on_valid_credentials  Bonus  No error banner shown
 test_tc83_full_login_flow [smoke]              1–4    Full E2E flow
───────────────────────────────────────────────────────────────────────────────
"""

import pytest
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID   = "TC-83"
TC_NAME = "Successful Login with Valid Username and Password"
TC_LINK = "SAUC-3 — User Login with Username and Password"


class TestTC83Login(BaseTest):
    """
    TC-83 | Successful Login with Valid Username and Password
    Priority: High | Status: New | Linked: SAUC-3
    URL: https://www.saucedemo.com/
    """

    # ------------------------------------------------------------------ #
    #  TC-83 Step 1 — Navigate and verify login page loads                #
    # ------------------------------------------------------------------ #
    def test_tc83_login_page_displayed(self, driver):
        """
        TC-83 Step 1:
        Navigate to https://www.saucedemo.com/ and verify the login page
        renders with all 3 required elements: username field, password
        field, and login button.

        Expected:
          ✅ id=user-name   — username input is visible
          ✅ id=password    — password input is visible
          ✅ id=login-button — login button is visible
        """
        logger.info(f"[{TC_ID}] ▶ Step 1 — Navigate to {Config.BASE_URL}")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)

        assert login_page.is_username_field_visible(), \
            f"[{TC_ID}] FAIL Step 1: id=user-name input is not visible"
        assert login_page.is_password_field_visible(), \
            f"[{TC_ID}] FAIL Step 1: id=password input is not visible"
        assert login_page.is_login_button_visible(), \
            f"[{TC_ID}] FAIL Step 1: id=login-button is not visible"

        logger.info(f"[{TC_ID}] ✅ Step 1 PASSED — All 3 login elements confirmed visible")

    # ------------------------------------------------------------------ #
    #  TC-83 Step 2 — Enter valid username                                 #
    # ------------------------------------------------------------------ #
    def test_tc83_enter_username(self, driver):
        """
        TC-83 Step 2:
        Type 'standard_user' into id=user-name and verify the field value.

        Expected:
          ✅ id=user-name value == 'standard_user'
        """
        logger.info(f"[{TC_ID}] ▶ Step 2 — Enter username '{Config.USERNAME}'")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.enter_username(Config.USERNAME)

        actual_value = login_page.get_username_value()
        assert actual_value == Config.USERNAME, \
            f"[{TC_ID}] FAIL Step 2: Expected '{Config.USERNAME}', got '{actual_value}'"

        logger.info(f"[{TC_ID}] ✅ Step 2 PASSED — Username value confirmed: '{actual_value}'")

    # ------------------------------------------------------------------ #
    #  TC-83 Step 3 — Enter valid password (masked)                        #
    # ------------------------------------------------------------------ #
    def test_tc83_enter_password(self, driver):
        """
        TC-83 Step 3:
        Type 'secret_sauce' into id=password and verify:
          a) Field type == 'password' (browser masks the value).
          b) Field value == expected credential.

        Expected:
          ✅ type attribute == 'password'
          ✅ value == 'secret_sauce'
        """
        logger.info(f"[{TC_ID}] ▶ Step 3 — Enter password (masked) into id=password")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.enter_password(Config.PASSWORD)

        field_type = login_page.get_password_field_type()
        assert field_type == "password", \
            f"[{TC_ID}] FAIL Step 3: type='{field_type}', expected 'password' (must be masked)"

        actual_value = login_page.get_password_value()
        assert actual_value == Config.PASSWORD, \
            f"[{TC_ID}] FAIL Step 3: Password value mismatch"

        logger.info(f"[{TC_ID}] ✅ Step 3 PASSED — type='password' ✔, value verified ✔")

    # ------------------------------------------------------------------ #
    #  TC-83 Step 4 — Click Login → redirect to inventory page            #
    # ------------------------------------------------------------------ #
    def test_tc83_successful_login_redirects_to_inventory(self, driver):
        """
        TC-83 Step 4:
        Enter valid credentials and click Login. Verify redirect and
        page content after successful authentication.

        Expected:
          ✅ URL contains 'inventory.html'
          ✅ Page header == 'Products'
          ✅ 6 inventory items rendered
          ✅ Shopping cart icon visible
        """
        logger.info(f"[{TC_ID}] ▶ Step 4 — Login and verify inventory.html redirect")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.login(Config.USERNAME, Config.PASSWORD)

        inventory_page = InventoryPage(driver)

        # Assert 1: URL redirect
        assert inventory_page.is_on_inventory_page(), \
            f"[{TC_ID}] FAIL Step 4: URL not inventory. Current: {driver.current_url}"

        # Assert 2: Page header
        page_header = inventory_page.get_page_header_title()
        assert page_header == "Products", \
            f"[{TC_ID}] FAIL Step 4: Header='{page_header}', expected 'Products'"

        # Assert 3: Inventory items
        item_count = inventory_page.get_inventory_item_count()
        assert item_count == 6, \
            f"[{TC_ID}] FAIL Step 4: {item_count} items found, expected 6"

        # Assert 4: Cart icon
        assert inventory_page.is_cart_icon_visible(), \
            f"[{TC_ID}] FAIL Step 4: Shopping cart icon not visible"

        logger.info(
            f"[{TC_ID}] ✅ Step 4 PASSED — "
            f"URL=inventory.html ✔ | Header='{page_header}' ✔ | "
            f"Items={item_count} ✔ | Cart=visible ✔"
        )

    # ------------------------------------------------------------------ #
    #  TC-83 Bonus — Verify no error banner on valid credentials           #
    # ------------------------------------------------------------------ #
    def test_tc83_login_no_error_on_valid_credentials(self, driver):
        """
        TC-83 Bonus Assertion:
        After successful login with valid credentials, verify no error
        banner is displayed on the login page.

        Expected:
          ✅ [data-test='error'] element is NOT visible
        """
        logger.info(f"[{TC_ID}] ▶ Bonus — Verify no error banner on valid credentials")
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        login_page.login(Config.USERNAME, Config.PASSWORD)

        error_displayed = login_page.is_error_displayed()
        assert not error_displayed, \
            f"[{TC_ID}] FAIL Bonus: Error banner unexpectedly shown after valid login"

        logger.info(f"[{TC_ID}] ✅ Bonus PASSED — No error banner confirmed ✔")

    # ------------------------------------------------------------------ #
    #  TC-83 Full E2E Smoke Test — Steps 1 → 4 combined                   #
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_tc83_full_login_flow(self, driver):
        """
        TC-83 SMOKE | Full end-to-end login flow (Steps 1–4 combined).

        Live Execution Verified:
          ✅ Step 1 | Login page loaded — all fields visible
          ✅ Step 2 | 'standard_user' entered into id=user-name
          ✅ Step 3 | type=password masked ✔, value confirmed ✔
          ✅ Step 4 | Redirected → inventory.html ✔
          ✅ Assert | Header='Products' ✔ | 6 items ✔ | Cart visible ✔
          ✅ Assert | No error banner shown ✔
        """
        logger.info(f"[{TC_ID}] ▶ SMOKE — Starting full E2E login flow (Steps 1–4)")

        # ── Step 1: Open login page ──────────────────────────────────── #
        login_page = LoginPage(driver)
        login_page.open(Config.BASE_URL)
        assert login_page.is_username_field_visible(), \
            f"[{TC_ID}] Step 1 FAIL: id=user-name not visible"
        assert login_page.is_password_field_visible(), \
            f"[{TC_ID}] Step 1 FAIL: id=password not visible"
        assert login_page.is_login_button_visible(), \
            f"[{TC_ID}] Step 1 FAIL: id=login-button not visible"
        logger.info(f"[{TC_ID}] SMOKE Step 1 ✅  Login page elements present")

        # ── Step 2: Enter username ───────────────────────────────────── #
        login_page.enter_username(Config.USERNAME)
        assert login_page.get_username_value() == Config.USERNAME, \
            f"[{TC_ID}] Step 2 FAIL: username value mismatch"
        logger.info(f"[{TC_ID}] SMOKE Step 2 ✅  Username '{Config.USERNAME}' entered")

        # ── Step 3: Enter password (masked) ─────────────────────────── #
        login_page.enter_password(Config.PASSWORD)
        assert login_page.get_password_field_type() == "password", \
            f"[{TC_ID}] Step 3 FAIL: password not masked (type != 'password')"
        logger.info(f"[{TC_ID}] SMOKE Step 3 ✅  Password entered, type='password' (masked)")

        # ── Step 4: Click Login → verify inventory ───────────────────── #
        login_page.click_login()
        inventory_page = InventoryPage(driver)

        assert inventory_page.is_on_inventory_page(), \
            f"[{TC_ID}] Step 4 FAIL: Not on inventory.html. URL={driver.current_url}"
        assert inventory_page.get_page_header_title() == "Products", \
            f"[{TC_ID}] Step 4 FAIL: Header != 'Products'"
        assert inventory_page.get_inventory_item_count() == 6, \
            f"[{TC_ID}] Step 4 FAIL: Item count != 6"
        assert inventory_page.is_cart_icon_visible(), \
            f"[{TC_ID}] Step 4 FAIL: Cart icon not visible"

        # ── Bonus: No error banner ───────────────────────────────────── #
        assert not login_page.is_error_displayed(), \
            f"[{TC_ID}] Bonus FAIL: Error banner shown unexpectedly"

        logger.info(
            f"[{TC_ID}] SMOKE ✅ PASSED — Full flow verified: "
            f"URL=inventory.html | Header=Products | Items=6 | "
            f"Cart=visible | No error banner"
        )
