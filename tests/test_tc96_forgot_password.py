"""
test_tc96_forgot_password.py
-----------------------------
Pytest test module for TC-96: Forgot Password Link is Visible on the Login Page.

QTest ID  : 11194308
Priority  : High (🔴)
URL       : https://www.saucedemo.com/
Requirement: SAUC-7 — Allow Users to Reset Their Password

Test Steps Covered:
  Step 1 — Navigate to login page and verify it loads.
  Step 2 — Check that the 'Forgot Password' link is visible.
  Step 3 — Click 'Forgot Password' and verify navigation to reset page.
  Full Flow — End-to-end test covering all 3 steps.

Expected Outcome vs Actual:
  ✅ Step 1 PASSES  — SauceDemo login page loads successfully.
  ❌ Step 2 FAILS   — No 'Forgot Password' element exists (0/13 strategies matched).
  ❌ Step 3 FAILS   — Cannot click absent element; navigation impossible.
  ❌ Full Flow FAILS — SAUC-7 is NOT implemented in SauceDemo.

Root Cause:
  SauceDemo does NOT have a 'Forgot Password' / password reset feature.
  The DOM contains 0 anchor tags and no element matching any of 13
  exhaustive selector strategies.
  Requirement SAUC-7 — Allow Users to Reset Their Password — is UNSATISFIED.
"""

import pytest
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.logger import get_logger

logger = get_logger("TC96_Tests")


@pytest.mark.tc96
@pytest.mark.high_priority
@pytest.mark.sauc7
class TestTC96ForgotPassword(BaseTest):
    """
    Test class for TC-96.
    Inherits BaseTest for automatic driver setup/teardown and screenshot-on-fail.
    """

    # ── Step 1 ────────────────────────────────────────────────────────────────

    @pytest.mark.step1
    def test_step1_login_page_is_displayed(self):
        """
        TC-96 | Step 1
        --------------
        Verify that navigating to https://www.saucedemo.com/ displays the
        login page with all expected form elements (username, password, button).

        Expected: Login page fully rendered with all form elements visible.
        Actual:   ✅ PASSES — SauceDemo login page loads successfully.
        """
        logger.info("TC-96 | Step 1 — Verifying login page is displayed.")

        login_page = LoginPage(self.driver)
        login_page.navigate_to_login()

        # Assert page URL
        current_url = login_page.get_current_url()
        assert "saucedemo.com" in current_url, (
            f"Expected URL to contain 'saucedemo.com', got: {current_url}"
        )

        # Assert all login form elements are visible
        assert login_page.is_login_page_displayed(), (
            "Login page elements (username / password / login button) are not all visible."
        )

        # Assert logo text
        logo_text = login_page.get_login_logo_text()
        assert logo_text, "Login logo/header text should not be empty."
        logger.info(f"Login logo text: '{logo_text}'")

        logger.info("✅ Step 1 PASSED — Login page displayed successfully.")

    # ── Step 2 ────────────────────────────────────────────────────────────────

    @pytest.mark.step2
    def test_step2_forgot_password_link_visible(self):
        """
        TC-96 | Step 2
        --------------
        Verify that a 'Forgot Password' link is clearly visible on the login page.

        Expected: 'Forgot Password' link is present and visible.
        Actual:   ❌ FAILS — 0 matches across all 13 selector strategies.

        Root Cause:
          SauceDemo does NOT implement a Forgot Password feature.
          Requirement SAUC-7 is UNIMPLEMENTED.
        """
        logger.info("TC-96 | Step 2 — Checking 'Forgot Password' link visibility.")

        login_page = LoginPage(self.driver)
        login_page.navigate_to_login()

        # Run the 13-strategy diagnostic report
        report = login_page.get_forgot_password_selector_report()
        total_matches = sum(report.values())

        logger.warning(f"Selector diagnostic report: {report}")
        logger.warning(f"Total matches across all 13 strategies: {total_matches}")
        logger.warning(
            f"Anchor tags on page: {login_page.get_anchor_tag_count()}"
        )

        # This assertion intentionally FAILS to surface SAUC-7 non-implementation
        assert login_page.is_forgot_password_visible(), (
            f"FAIL — TC-96 Step 2: 'Forgot Password' link is NOT visible on the login page. "
            f"Tried {len(report)} selector strategies, total matches: {total_matches}. "
            f"Requirement SAUC-7 (Allow Users to Reset Their Password) is NOT satisfied. "
            f"Selector report: {report}"
        )

        logger.info("✅ Step 2 PASSED — 'Forgot Password' link is visible.")

    # ── Step 3 ────────────────────────────────────────────────────────────────

    @pytest.mark.step3
    def test_step3_forgot_password_click_navigates(self):
        """
        TC-96 | Step 3
        --------------
        Click the 'Forgot Password' link and verify navigation to a
        password-reset page (URL should contain 'forgot' or 'reset').

        Expected: Browser navigates to a password reset / forgot-password page.
        Actual:   ❌ FAILS — Element is absent; cannot click.

        Root Cause:
          Step 2 already proves the element is absent.
          Without the element, navigation to a reset page is impossible.
          SAUC-7 is UNIMPLEMENTED.
        """
        logger.info("TC-96 | Step 3 — Clicking 'Forgot Password' and verifying navigation.")

        login_page = LoginPage(self.driver)
        login_page.navigate_to_login()

        # Attempt to click — will raise AssertionError if element absent
        login_page.click_forgot_password()

        # If click somehow succeeded, verify navigation
        current_url = login_page.get_current_url()
        logger.info(f"URL after clicking Forgot Password: {current_url}")

        navigated = any(
            keyword in current_url.lower()
            for keyword in ["forgot", "reset", "password"]
        )
        assert navigated, (
            f"FAIL — TC-96 Step 3: After clicking 'Forgot Password', expected URL to "
            f"contain 'forgot', 'reset', or 'password'. Actual URL: {current_url}"
        )

        logger.info("✅ Step 3 PASSED — Successfully navigated to password reset page.")

    # ── Full Flow ─────────────────────────────────────────────────────────────

    @pytest.mark.full_flow
    def test_tc96_forgot_password_link_full_flow(self):
        """
        TC-96 | Full End-to-End Flow
        ----------------------------
        Combines all 3 test steps into a single end-to-end test:
          1. Navigate to login page → verify load.
          2. Verify 'Forgot Password' link is visible.
          3. Click it → verify navigation to reset page.

        Expected: Full flow completes — login loads, link is visible, click navigates.
        Actual:   ❌ FAILS at Step 2 — element absent, SAUC-7 unimplemented.

        Screenshot: Auto-captured by conftest.py on failure.
        """
        logger.info("TC-96 | Full Flow — Starting end-to-end test.")

        login_page = LoginPage(self.driver)

        # ── Step 1: Navigate and verify login page ─────────────────────────
        logger.info("  [Step 1] Navigating to login page...")
        login_page.navigate_to_login()

        assert "saucedemo.com" in login_page.get_current_url(), (
            "Step 1 FAIL — Not on SauceDemo login page."
        )
        assert login_page.is_login_page_displayed(), (
            "Step 1 FAIL — Login form elements not fully visible."
        )
        logger.info("  ✅ Step 1 PASS — Login page loaded.")

        # ── Step 2: Verify 'Forgot Password' link visibility ───────────────
        logger.info("  [Step 2] Checking 'Forgot Password' link visibility...")
        report = login_page.get_forgot_password_selector_report()
        total_matches = sum(report.values())

        assert login_page.is_forgot_password_visible(), (
            f"Step 2 FAIL — 'Forgot Password' link NOT found on login page. "
            f"Strategies tried: {len(report)}, total matches: {total_matches}. "
            f"Report: {report}. "
            f"SAUC-7 (Allow Users to Reset Their Password) is NOT implemented."
        )
        logger.info("  ✅ Step 2 PASS — 'Forgot Password' link visible.")

        # ── Step 3: Click link and verify navigation ───────────────────────
        logger.info("  [Step 3] Clicking 'Forgot Password' and checking navigation...")
        login_page.click_forgot_password()

        current_url = login_page.get_current_url()
        assert any(
            kw in current_url.lower() for kw in ["forgot", "reset", "password"]
        ), (
            f"Step 3 FAIL — URL after click does not indicate a reset page. "
            f"Current URL: {current_url}"
        )
        logger.info(f"  ✅ Step 3 PASS — Navigated to: {current_url}")

        logger.info("✅ TC-96 Full Flow PASSED.")
