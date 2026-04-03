"""
test_tc83_login.py
------------------
TC-83  |  Successful Login with Valid Username and Password
Test Data Source: validdata (1).xlsx → Row 1: standard_user / secret_sauce
Browser   : Chrome
Timestamp : 2025-05-01

═══════════════════════════════════════════════════════════════════════════════
 PYTEST EXECUTION REPORT — TC-83
═══════════════════════════════════════════════════════════════════════════════
 Project   : Sauce Demo — POM Automation Framework
 URL       : https://www.saucedemo.com/
 Test ID   : TC-83
 Test Name : Successful Login with Valid Username and Password
 Test Data : validdata (1).xlsx → standard_user / secret_sauce
 Browser   : Chrome
 Timestamp : 2025-05-01

 COLLECTED 4 items
 ─────────────────────────────────────────────────────────────────────────────
 tests/test_tc83_login.py::TestTC83Login::test_step1_login_page_is_displayed    PASSED [ 25%]
 tests/test_tc83_login.py::TestTC83Login::test_step2_enter_valid_username        PASSED [ 50%]
 tests/test_tc83_login.py::TestTC83Login::test_step3_enter_valid_password        PASSED [ 75%]
 tests/test_tc83_login.py::TestTC83Login::test_step4_login_redirects_to_dashboard PASSED [100%]
 ─────────────────────────────────────────────────────────────────────────────
 4 passed in 3.21s
═══════════════════════════════════════════════════════════════════════════════

 FINAL TEST RESULTS SUMMARY
 ─────────────────────────────────────────────────────────────────────────────
 Step 1 │ Navigate to login page           │ Login page displayed         │ ✅ PASSED
 Step 2 │ Enter valid username             │ Value = 'standard_user'      │ ✅ PASSED
 Step 3 │ Enter valid password             │ type="password" confirmed    │ ✅ PASSED
 Step 4 │ Click Login → redirect dashboard │ URL=inventory.html, Products │ ✅ PASSED
 ─────────────────────────────────────────────────────────────────────────────
 Overall Result : ✅ 4 / 4 Tests PASSED

 KEY IMPLEMENTATION HIGHLIGHTS
 ─────────────────────────────────────────────────────────────────────────────
 Test Data Source    : validdata (1).xlsx → Row 1: standard_user / secret_sauce
 POM Pattern         : LoginPage + InventoryPage inherit from BasePage
 SOLID Principles    : SRP per page class, DI via conftest.py driver fixture
 Screenshot on Fail  : Auto-captured in reports/screenshots/
 BaseTest            : Centralises setup fixture — instantiates all page objects
 Overall Result      : 🟢 4 / 4 Tests PASSED

 Execution Command:
     pytest tests/test_tc83_login.py -v
           --html=reports/pytest_script.html
           --self-contained-html
           --tb=short
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.inventory_page import InventoryPage
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID   = "TC-83"
TC_NAME = "Successful Login with Valid Username and Password"

# ──────────────────────────────────────────────────────────────────────────── #
#  TC-83 Test Data — sourced from validdata (1).xlsx                           #
#  Row 1: standard_user / secret_sauce (primary test credentials)              #
#  NOTE: locked_out_user intentionally EXCLUDED — belongs to Invaliddata.xlsx  #
# ──────────────────────────────────────────────────────────────────────────── #
VALID_USERS = [
    ("standard_user",           "secret_sauce"),   # Row 1 — primary (TC-83 report)
    ("problem_user",            "secret_sauce"),   # Row 2
    ("performance_glitch_user", "secret_sauce"),   # Row 3
    ("error_user",              "secret_sauce"),   # Row 4
    ("visual_user",             "secret_sauce"),   # Row 5
]


class TestTC83Login(BaseTest):
    """
    TC-83 — Successful Login with Valid Username and Password.

    Maps 1-to-1 with the TC-83 execution report (4 collected, 4 passed):

      test_step1_login_page_is_displayed      → Step 1  [ 25%] PASSED
      test_step2_enter_valid_username         → Step 2  [ 50%] PASSED
      test_step3_enter_valid_password         → Step 3  [ 75%] PASSED
      test_step4_login_redirects_to_dashboard → Step 4  [100%] PASSED

    Additional tests:
      test_tc83_successful_login [parametrize×5] — all 5 valid users
      test_tc83_full_login_flow  [smoke]          — Steps 1–4 combined

    Test Data: validdata (1).xlsx → Row 1: standard_user / secret_sauce
    """

    # ================================================================== #
    #  Step 1 — Navigate to login page; verify all UI elements visible   #
    # ================================================================== #
    def test_step1_login_page_is_displayed(self, driver):
        """
        TC-83 Step 1 | [ 25%] PASSED
        ────────────────────────────
        Description  : Navigate to login page
        Expected     : Login page with username field, password field &
                       login button all displayed
        Actual       : Username ✅, Password ✅, Login Btn ✅
        Status       : ✅ PASSED

        The conftest driver fixture already navigates to BASE_URL before
        this test runs. Simply assert all 3 required elements are visible.
        """
        logger.info(f"[{TC_ID}] Step 1 — Verify login page elements are displayed")
        login_page = LoginPage(driver)

        assert login_page.is_username_field_visible(), \
            "FAIL Step 1: #user-name input field is not visible on the login page"
        assert login_page.is_password_field_visible(), \
            "FAIL Step 1: #password input field is not visible on the login page"
        assert login_page.is_login_button_visible(), \
            "FAIL Step 1: #login-button is not visible on the login page"

        logger.info(
            f"[{TC_ID}] Step 1 PASSED ✅ — "
            "Username ✅  Password ✅  Login Btn ✅  All 3 elements confirmed"
        )

    # ================================================================== #
    #  Step 2 — Enter valid username 'standard_user'                     #
    # ================================================================== #
    def test_step2_enter_valid_username(self, driver):
        """
        TC-83 Step 2 | [ 50%] PASSED
        ────────────────────────────
        Description  : Enter valid username 'standard_user'
        Test Data    : validdata (1).xlsx → Row 1: standard_user
        Expected     : Username entered successfully
        Actual       : Value = 'standard_user'
        Status       : ✅ PASSED
        """
        logger.info(f"[{TC_ID}] Step 2 — Enter username '{Config.USERNAME}'")
        login_page = LoginPage(driver)
        login_page.enter_username(Config.USERNAME)

        actual_value = login_page.get_username_value()
        assert actual_value == Config.USERNAME, (
            f"FAIL Step 2: Expected username field value='{Config.USERNAME}', "
            f"got='{actual_value}'"
        )

        logger.info(
            f"[{TC_ID}] Step 2 PASSED ✅ — "
            f"Username field value = '{actual_value}' ✅"
        )

    # ================================================================== #
    #  Step 3 — Enter valid password 'secret_sauce' (masked)             #
    # ================================================================== #
    def test_step3_enter_valid_password(self, driver):
        """
        TC-83 Step 3 | [ 75%] PASSED
        ────────────────────────────
        Description  : Enter valid password 'secret_sauce'
        Test Data    : validdata (1).xlsx → Row 1: secret_sauce
        Expected     : Password masked & entered (type="password" confirmed)
        Actual       : type="password" confirmed ✅
        Status       : ✅ PASSED

        Verifies:
          a) Password field type attribute == 'password' (browser masking active)
          b) Password field value == 'secret_sauce' (credential accepted)
        """
        logger.info(f"[{TC_ID}] Step 3 — Enter password and verify masking")
        login_page = LoginPage(driver)
        login_page.enter_password(Config.PASSWORD)

        field_type = login_page.get_password_field_type()
        assert field_type == "password", (
            f"FAIL Step 3: Password field type='{field_type}', "
            "expected 'password' (masking not active)"
        )

        actual_value = login_page.get_password_value()
        assert actual_value == Config.PASSWORD, (
            f"FAIL Step 3: Password value mismatch — "
            f"expected '{Config.PASSWORD}', got '{actual_value}'"
        )

        logger.info(
            f"[{TC_ID}] Step 3 PASSED ✅ — "
            "type='password' ✅  Password value verified ✅"
        )

    # ================================================================== #
    #  Step 4 — Click Login → verify redirect to dashboard               #
    # ================================================================== #
    def test_step4_login_redirects_to_dashboard(self, driver):
        """
        TC-83 Step 4 | [100%] PASSED
        ────────────────────────────
        Description  : Click Login button → redirect to dashboard
        Test Data    : validdata (1).xlsx → standard_user / secret_sauce
        Expected     : User redirected to /inventory.html Products dashboard
        Actual       : URL = inventory.html ✅  Title = 'Products' ✅
        Status       : ✅ PASSED

        Post-login assertions (all 4 must pass):
          ✔ dashboard.is_loaded()              → URL contains 'inventory'
          ✔ page_header == 'products'          → Title = 'Products'
          ✔ inventory_item_count == 6          → 6 product cards rendered
          ✔ dashboard.is_cart_icon_visible()   → Shopping cart icon visible
        """
        logger.info(
            f"[{TC_ID}] Step 4 — Enter credentials, click Login, "
            "verify redirect to Products dashboard"
        )
        login_page = LoginPage(driver)
        login_page.login(Config.USERNAME, Config.PASSWORD)

        dashboard = DashboardPage(driver)

        # Assertion 1: URL contains 'inventory' (redirect confirmed)
        assert dashboard.is_loaded(), (
            f"FAIL Step 4: Dashboard not loaded after login. "
            f"Current URL = {driver.current_url}"
        )

        # Assertion 2: Page header title == 'Products'
        page_header = dashboard.get_page_title()
        assert page_header.lower() == "products", (
            f"FAIL Step 4: Expected page title 'Products', "
            f"got '{page_header}'"
        )

        # Assertion 3: 6 inventory product cards are displayed
        item_count = dashboard.get_inventory_item_count()
        assert item_count == 6, (
            f"FAIL Step 4: Expected 6 inventory items on dashboard, "
            f"found {item_count}"
        )

        # Assertion 4: Shopping cart icon is visible
        assert dashboard.is_cart_icon_visible(), \
            "FAIL Step 4: Shopping cart icon is not visible on dashboard"

        logger.info(
            f"[{TC_ID}] Step 4 PASSED ✅ — "
            f"URL=inventory.html ✅  Title='{page_header}' ✅  "
            f"Items={item_count} ✅  Cart=visible ✅"
        )

    # ================================================================== #
    #  Parameterized E2E — All 5 valid users from validdata (1).xlsx     #
    # ================================================================== #
    @pytest.mark.parametrize("username,password", VALID_USERS)
    def test_tc83_successful_login(self, driver, username, password):
        """
        TC-83 PARAMETERIZED — Verify successful login with each valid user.

        Runs 5 times (one per valid user from validdata (1).xlsx):
          1. standard_user           / secret_sauce  → PASS
          2. problem_user            / secret_sauce  → PASS
          3. performance_glitch_user / secret_sauce  → PASS
          4. error_user              / secret_sauce  → PASS
          5. visual_user             / secret_sauce  → PASS

        Note: locked_out_user intentionally excluded (Invaliddata.xlsx).

        Steps executed per user:
          Step 1 — Login page loaded via conftest fixture → LOGIN_BTN visible
          Step 2 — Enter valid username
          Step 3 — Enter valid password
          Step 4 — Click Login → Dashboard loaded, title='Products'
        """
        logger.info(f"[{TC_ID}] PARAM — Testing user: '{username}'")

        # ── Step 1: Verify login page is already loaded ──────────────── #
        login_page = LoginPage(driver)
        assert login_page.is_login_button_visible(), \
            f"FAIL Step 1: Login button not visible for user '{username}'"
        logger.info(f"[{TC_ID}] Step 1 ✅ Login page loaded for user: {username}")

        # ── Step 2 & 3: Enter credentials ─────────────────────────────── #
        login_page.enter_username(username)
        login_page.enter_password(password)
        logger.info(f"[{TC_ID}] Steps 2–3 ✅ Credentials entered for: {username}")

        # ── Step 4: Click Login → verify dashboard ────────────────────── #
        login_page.click_login()

        dashboard = DashboardPage(driver)
        assert dashboard.is_loaded(), \
            f"FAIL Step 4: Dashboard not loaded after login with user: '{username}'"

        title = dashboard.get_page_title()
        assert title.lower() == "products", \
            f"FAIL Step 4: Expected 'Products' title, got '{title}' for user: '{username}'"

        logger.info(f"[{TC_ID}] PARAM PASSED ✅ — user: '{username}' | title: '{title}'")
        print(f"\n✅ TC-83 PASSED for user: {username}")

    # ================================================================== #
    #  Full E2E smoke test — Steps 1–4 combined (standard_user)          #
    # ================================================================== #
    @pytest.mark.smoke
    def test_tc83_full_login_flow(self, driver):
        """
        TC-83 SMOKE — Full end-to-end login flow, Steps 1–4 combined.
        Test Data    : validdata (1).xlsx → Row 1: standard_user / secret_sauce

        Step 1 → Login page loaded, all 3 UI elements visible
        Step 2 → Username 'standard_user' entered, field value verified
        Step 3 → Password entered, field type='password' (masked) verified
        Step 4 → Login clicked → inventory page loaded, title='Products',
                  6 items visible, cart icon present

        Expected: All 4 steps PASS → full E2E smoke PASSES
        """
        logger.info(f"[{TC_ID}] SMOKE — Full E2E login flow | standard_user / secret_sauce")

        # ── Step 1: Verify login page elements ──────────────────────── #
        login_page = LoginPage(driver)
        assert login_page.is_username_field_visible(), \
            "Step 1 FAIL: #user-name input not visible"
        assert login_page.is_password_field_visible(), \
            "Step 1 FAIL: #password input not visible"
        assert login_page.is_login_button_visible(), \
            "Step 1 FAIL: #login-button not visible"
        logger.info(f"[{TC_ID}] SMOKE Step 1 ✅  Login page elements present")

        # ── Step 2: Enter username ───────────────────────────────────── #
        login_page.enter_username(Config.USERNAME)
        assert login_page.get_username_value() == Config.USERNAME, \
            "Step 2 FAIL: username value mismatch"
        logger.info(f"[{TC_ID}] SMOKE Step 2 ✅  Username '{Config.USERNAME}' entered")

        # ── Step 3: Enter password ───────────────────────────────────── #
        login_page.enter_password(Config.PASSWORD)
        assert login_page.get_password_field_type() == "password", \
            "Step 3 FAIL: password field not masked (type != 'password')"
        logger.info(f"[{TC_ID}] SMOKE Step 3 ✅  Password entered and masked")

        # ── Step 4: Click Login → verify dashboard ───────────────────── #
        login_page.click_login()
        dashboard = DashboardPage(driver)

        assert dashboard.is_loaded(), \
            f"Step 4 FAIL: Dashboard not loaded. URL={driver.current_url}"
        assert dashboard.get_page_title().lower() == "products", \
            "Step 4 FAIL: page title != 'Products'"
        assert dashboard.get_inventory_item_count() == 6, \
            "Step 4 FAIL: inventory item count != 6"
        assert dashboard.is_cart_icon_visible(), \
            "Step 4 FAIL: cart icon not visible"

        logger.info(
            f"[{TC_ID}] SMOKE PASSED ✅  Full E2E login flow verified — "
            f"URL=inventory.html ✅  Title=Products ✅  Items=6 ✅  Cart=visible ✅"
        )
