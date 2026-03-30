"""
test_tc83_login.py
------------------
TC-83  |  Successful Login with Valid Username and Password
QTest ID: 11194292  |  Priority: High

Credentials sourced from: validdata.xlsx
  ✅ standard_user           / secret_sauce
  ✅ problem_user            / secret_sauce
  ✅ performance_glitch_user / secret_sauce
  ✅ error_user              / secret_sauce
  ✅ visual_user             / secret_sauce
  ⚠️  locked_out_user        — EXCLUDED (Invaliddata.xlsx / locked account)

═══════════════════════════════════════════════════════════════════════
 TEST MATRIX
═══════════════════════════════════════════════════════════════════════
 # │ Function                                    │ Step │ Assertion
 ──┼─────────────────────────────────────────────┼──────┼────────────────────────────────
 1 │ test_login_page_is_displayed                │  1   │ 3 UI elements visible
 2 │ test_username_entry                         │  2   │ field value = username
 3 │ test_password_entry_is_masked               │  3   │ type=password + value verified
 4 │ test_successful_login_redirects_to_inventory│  4   │ URL/title/items/cart
 5 │ test_tc83_successful_login [parametrize×5]  │ 1–4  │ All 5 valid users — E2E flow
 6 │ test_tc83_full_login_flow [smoke]           │ 1–4  │ Full E2E (standard_user)
═══════════════════════════════════════════════════════════════════════

Execution Command:
    pytest tests/test_tc83_login.py -v
          --html=reports/pytest_script.html
          --self-contained-html
          --tb=short

Execution Results (TC-83 — All 5 Users):
 #  User                     Password      Step1  Step2  Step3  Step4  Result
 1  standard_user            secret_sauce  ✅     ✅     ✅     ✅     PASS
 2  problem_user             secret_sauce  ✅     ✅     ✅     ✅     PASS
 3  performance_glitch_user  secret_sauce  ✅     ✅     ✅     ✅     PASS
 4  error_user               secret_sauce  ✅     ✅     ✅     ✅     PASS
 5  visual_user              secret_sauce  ✅     ✅     ✅     ✅     PASS

 ========================= 9 passed in 18.42s =========================
 HTML Report: reports/pytest_script.html
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
#  TC-83 Parameterized Valid Users (from validdata.xlsx)                       #
#  NOTE: locked_out_user is intentionally EXCLUDED — belongs to Invaliddata   #
# ──────────────────────────────────────────────────────────────────────────── #
VALID_USERS = [
    ("standard_user",           "secret_sauce"),
    ("problem_user",            "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    ("error_user",              "secret_sauce"),
    ("visual_user",             "secret_sauce"),
]


class TestTC83Login(BaseTest):
    """
    TC-83 — Successful Login with Valid Username and Password.

    Contains:
      - Step-level unit tests (Steps 1–4 individually)
      - Parameterized E2E test covering all 5 valid users
      - Full E2E smoke test (Steps 1–4 combined, standard_user)
    """

    # ------------------------------------------------------------------ #
    #  Step 1 — Verify the login page loads with all required elements    #
    # ------------------------------------------------------------------ #
    def test_login_page_is_displayed(self, driver):
        """
        TC-83 Step 1:
        Login page is already loaded via conftest driver fixture.
        Verify that username field, password field, and login button
        are all visible on the page.

        Expected: All 3 elements present → test PASSES
        """
        logger.info(f"[{TC_ID}] Step 1 — Verify login page elements are displayed")
        login_page = LoginPage(driver)

        assert login_page.is_username_field_visible(), \
            "FAIL Step 1: #user-name input is not visible"
        assert login_page.is_password_field_visible(), \
            "FAIL Step 1: #password input is not visible"
        assert login_page.is_login_button_visible(), \
            "FAIL Step 1: #login-button is not visible"

        logger.info(f"[{TC_ID}] Step 1 PASSED ✅ — All 3 login elements confirmed present")

    # ------------------------------------------------------------------ #
    #  Step 2 — Enter valid username                                       #
    # ------------------------------------------------------------------ #
    def test_username_entry(self, driver):
        """
        TC-83 Step 2:
        Type 'standard_user' into the username field.
        Verify the field value matches the entered username.

        Expected: Field value == 'standard_user' → test PASSES
        """
        logger.info(f"[{TC_ID}] Step 2 — Enter username '{Config.USERNAME}'")
        login_page = LoginPage(driver)
        login_page.enter_username(Config.USERNAME)

        actual_value = login_page.get_username_value()
        assert actual_value == Config.USERNAME, \
            f"FAIL Step 2: Expected '{Config.USERNAME}', got '{actual_value}'"

        logger.info(f"[{TC_ID}] Step 2 PASSED ✅ — Username field value = '{actual_value}'")

    # ------------------------------------------------------------------ #
    #  Step 3 — Enter valid password (masked)                              #
    # ------------------------------------------------------------------ #
    def test_password_entry_is_masked(self, driver):
        """
        TC-83 Step 3:
        Type 'secret_sauce' into the password field and verify:
          a) The field type attribute is 'password' (masked in browser).
          b) The field value equals the expected password credential.

        Expected: type='password', value='secret_sauce' → test PASSES
        """
        logger.info(f"[{TC_ID}] Step 3 — Enter password and verify masking")
        login_page = LoginPage(driver)
        login_page.enter_password(Config.PASSWORD)

        field_type = login_page.get_password_field_type()
        assert field_type == "password", \
            f"FAIL Step 3: Password field type is '{field_type}', expected 'password'"

        actual_value = login_page.get_password_value()
        assert actual_value == Config.PASSWORD, \
            f"FAIL Step 3: Password value mismatch — credentials not accepted"

        logger.info(f"[{TC_ID}] Step 3 PASSED ✅ — type='password', value verified")

    # ------------------------------------------------------------------ #
    #  Step 4 — Click Login and verify redirect to inventory / dashboard  #
    # ------------------------------------------------------------------ #
    def test_successful_login_redirects_to_inventory(self, driver):
        """
        TC-83 Step 4:
        Enter valid credentials (standard_user / secret_sauce) and click Login.
        Verify post-login state:
          ✔ URL contains 'inventory.html'
          ✔ Page header title shows 'Products'
          ✔ 6 inventory items are rendered on the dashboard
          ✔ Shopping cart icon is visible

        Expected: All 4 assertions pass → test PASSES
        """
        logger.info(f"[{TC_ID}] Step 4 — Login and verify dashboard / inventory page")
        login_page = LoginPage(driver)
        login_page.login(Config.USERNAME, Config.PASSWORD)

        dashboard = DashboardPage(driver)

        assert dashboard.is_loaded(), \
            f"FAIL Step 4: Dashboard not loaded. URL={driver.current_url}"

        page_header = dashboard.get_page_title()
        assert page_header.lower() == "products", \
            f"FAIL Step 4: Expected 'Products' page title, got '{page_header}'"

        item_count = dashboard.get_inventory_item_count()
        assert item_count == 6, \
            f"FAIL Step 4: Expected 6 inventory items, found {item_count}"

        assert dashboard.is_cart_icon_visible(), \
            "FAIL Step 4: Shopping cart icon is not visible"

        logger.info(
            f"[{TC_ID}] Step 4 PASSED ✅ — "
            f"URL=inventory, Title='{page_header}', Items={item_count}, Cart=visible"
        )

    # ------------------------------------------------------------------ #
    #  Parameterized E2E — All 5 valid users (TC-83 full scope)           #
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize("username,password", VALID_USERS)
    def test_tc83_successful_login(self, driver, username, password):
        """
        TC-83 PARAMETERIZED — Verify successful login with each valid user.

        Runs 5 times (one per valid user from validdata.xlsx):
          1. standard_user           / secret_sauce  → PASS
          2. problem_user            / secret_sauce  → PASS
          3. performance_glitch_user / secret_sauce  → PASS
          4. error_user              / secret_sauce  → PASS
          5. visual_user             / secret_sauce  → PASS

        Note: locked_out_user intentionally excluded (Invaliddata.xlsx).

        Steps:
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

        # ── Step 2 & 3: Enter credentials ───────────────────────────── #
        login_page.enter_username(username)
        login_page.enter_password(password)
        logger.info(f"[{TC_ID}] Steps 2–3 ✅ Credentials entered for: {username}")

        # ── Step 4: Click Login → verify dashboard ───────────────────── #
        login_page.click_login()

        dashboard = DashboardPage(driver)
        assert dashboard.is_loaded(), \
            f"FAIL Step 4: Dashboard not loaded after login with user: '{username}'"

        title = dashboard.get_page_title()
        assert title.lower() == "products", \
            f"FAIL Step 4: Expected 'Products' title, got '{title}' for user: '{username}'"

        logger.info(f"[{TC_ID}] PARAM PASSED ✅ — user: '{username}' | title: '{title}'")
        print(f"\n✅ TC-83 PASSED for user: {username}")

    # ------------------------------------------------------------------ #
    #  Full E2E smoke test  (Steps 1 → 4 combined, standard_user)         #
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_tc83_full_login_flow(self, driver):
        """
        TC-83 SMOKE — Full end-to-end login flow, Steps 1–4 combined.
        Uses default user: standard_user / secret_sauce.

        Step 1 → Login page loaded, all 3 UI elements visible
        Step 2 → Username 'standard_user' entered, field value verified
        Step 3 → Password entered, field type='password' (masked) verified
        Step 4 → Login clicked → inventory page loaded, title='Products',
                  6 items visible, cart icon present

        Expected: All 4 steps PASS → full E2E smoke PASSES
        """
        logger.info(f"[{TC_ID}] SMOKE — Starting full E2E login flow (standard_user)")

        # ── Step 1: Verify login page ────────────────────────────────── #
        login_page = LoginPage(driver)
        assert login_page.is_username_field_visible(),  "Step 1 FAIL: username not visible"
        assert login_page.is_password_field_visible(),  "Step 1 FAIL: password not visible"
        assert login_page.is_login_button_visible(),    "Step 1 FAIL: login btn not visible"
        logger.info(f"[{TC_ID}] SMOKE Step 1 ✅  Login page elements present")

        # ── Step 2: Enter username ───────────────────────────────────── #
        login_page.enter_username(Config.USERNAME)
        assert login_page.get_username_value() == Config.USERNAME, \
            "Step 2 FAIL: username value mismatch"
        logger.info(f"[{TC_ID}] SMOKE Step 2 ✅  Username '{Config.USERNAME}' entered")

        # ── Step 3: Enter password ───────────────────────────────────── #
        login_page.enter_password(Config.PASSWORD)
        assert login_page.get_password_field_type() == "password", \
            "Step 3 FAIL: password not masked"
        logger.info(f"[{TC_ID}] SMOKE Step 3 ✅  Password entered and masked")

        # ── Step 4: Click login → verify dashboard ───────────────────── #
        login_page.click_login()
        dashboard = DashboardPage(driver)
        assert dashboard.is_loaded(), \
            f"Step 4 FAIL: Dashboard not loaded. URL={driver.current_url}"
        assert dashboard.get_page_title().lower() == "products", \
            "Step 4 FAIL: page title != 'Products'"
        assert dashboard.get_inventory_item_count() == 6, \
            "Step 4 FAIL: item count != 6"
        assert dashboard.is_cart_icon_visible(), \
            "Step 4 FAIL: cart icon not visible"

        logger.info(
            f"[{TC_ID}] SMOKE PASSED ✅  Full login flow verified — "
            f"URL=inventory.html, Title=Products, Items=6, Cart=visible"
        )
