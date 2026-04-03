"""
login_page.py
-------------
Page Object Model for the SauceDemo Login Page.
Implements all locator strategies used in TC-96 to detect the
'Forgot Password' link (or confirm its absence).

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
Linked Requirement: SAUC-7 — Allow Users to Reset Their Password
URL: https://www.saucedemo.com/
"""

from typing import Optional, List, Dict, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    POM class representing the SauceDemo Login Page.

    Provides:
    - Standard login form element locators
    - 13 exhaustive selector strategies for detecting the 'Forgot Password' element
    - Helper methods used across TC-96 test steps
    """

    # ── Page URL ──────────────────────────────────────────────────────────────
    PAGE_URL: str = "https://www.saucedemo.com/"

    # ── Standard Login Form Locators ──────────────────────────────────────────
    USERNAME_INPUT      = (By.ID, "user-name")
    PASSWORD_INPUT      = (By.ID, "password")
    LOGIN_BUTTON        = (By.ID, "login-button")
    LOGIN_LOGO          = (By.CLASS_NAME, "login_logo")
    ERROR_MESSAGE       = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_WRAPPER       = (By.CLASS_NAME, "login_wrapper")
    LOGIN_FORM          = (By.TAG_NAME, "form")

    # ── Forgot Password Selector Strategies (13 total) ───────────────────────
    # These represent every reasonable approach to locate a 'Forgot Password'
    # link.  All 13 return 0 matches on SauceDemo, proving SAUC-7 is absent.

    _FORGOT_SELECTORS: List[Tuple[str, str, str]] = [
        # Strategy 1 — Exact link text
        ("LINK_TEXT",         By.LINK_TEXT,         "Forgot Password"),
        # Strategy 2 — Partial link text
        ("PARTIAL_LINK_TEXT", By.PARTIAL_LINK_TEXT,  "Forgot"),
        # Strategy 3 — XPath text() match
        ("XPATH_TEXT",        By.XPATH,             "//*[contains(text(),'Forgot')]"),
        # Strategy 4 — XPath anchor href containing 'forgot'
        ("XPATH_HREF",        By.XPATH,             "//a[contains(@href,'forgot')]"),
        # Strategy 5 — CSS anchor href
        ("CSS_HREF",          By.CSS_SELECTOR,      "a[href*='forgot']"),
        # Strategy 6 — CSS class containing 'forgot'
        ("CSS_CLASS",         By.CSS_SELECTOR,      "[class*='forgot']"),
        # Strategy 7 — CSS ID containing 'forgot'
        ("CSS_ID",            By.CSS_SELECTOR,      "[id*='forgot']"),
        # Strategy 8 — Button with 'forgot' text
        ("BUTTON_TEXT",       By.XPATH,             "//button[contains(text(),'Forgot')]"),
        # Strategy 9 — Span with 'forgot' text
        ("SPAN_TEXT",         By.XPATH,             "//span[contains(text(),'Forgot')]"),
        # Strategy 10 — Anchor tag with 'reset' in href
        ("RESET_HREF",        By.CSS_SELECTOR,      "a[href*='reset']"),
        # Strategy 11 — Any element with 'password' in href
        ("PASSWORD_HREF",     By.CSS_SELECTOR,      "a[href*='password']"),
        # Strategy 12 — XPath case-insensitive 'forgot' in text
        ("XPATH_LOWER",       By.XPATH,             "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'forgot')]"),
        # Strategy 13 — Any anchor tag on the page
        ("ALL_ANCHORS",       By.TAG_NAME,          "a"),
    ]

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate_to_login(self) -> None:
        """Opens the SauceDemo login page."""
        self.open(self.PAGE_URL)
        self._logger.info("Navigated to SauceDemo login page.")

    # ── Login Form Helpers ────────────────────────────────────────────────────

    def is_login_page_displayed(self) -> bool:
        """
        Verifies that the login page is fully loaded by checking for
        the username input, password input, and login button.

        Returns:
            bool: True if all core login elements are present and visible.
        """
        checks = [
            self.is_element_displayed(self.USERNAME_INPUT),
            self.is_element_displayed(self.PASSWORD_INPUT),
            self.is_element_displayed(self.LOGIN_BUTTON),
        ]
        result = all(checks)
        self._logger.info(
            f"Login page displayed check — username:{checks[0]}, "
            f"password:{checks[1]}, login_btn:{checks[2]} → {result}"
        )
        return result

    def get_login_logo_text(self) -> str:
        """Returns the text of the login page logo/header."""
        return self.get_text(self.LOGIN_LOGO)

    def enter_username(self, username: str) -> None:
        """Types the given username into the username field."""
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Types the given password into the password field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Clicks the Login button."""
        self.click(self.LOGIN_BUTTON)

    # ── Forgot Password Detection ─────────────────────────────────────────────

    def find_forgot_password_element(self) -> Optional[WebElement]:
        """
        Iterates through all 13 selector strategies to find any element
        that could represent a 'Forgot Password' feature.

        Returns:
            Optional[WebElement]: First matching element found, or None if absent.
        """
        self._logger.info("Starting 13-strategy Forgot Password element search...")

        for strategy_name, by, value in self._FORGOT_SELECTORS:
            elements = self._driver.find_elements(by, value)
            self._logger.debug(
                f"  Strategy [{strategy_name}] — by={by}, value='{value}' → {len(elements)} match(es)"
            )
            if elements:
                self._logger.warning(
                    f"  ✅ Match found via [{strategy_name}]: {elements[0].tag_name} "
                    f"text='{elements[0].text}'"
                )
                return elements[0]

        self._logger.warning(
            "❌ All 13 strategies exhausted — NO 'Forgot Password' element found. "
            "SAUC-7 appears UNIMPLEMENTED."
        )
        return None

    def get_forgot_password_selector_report(self) -> Dict[str, int]:
        """
        Runs all 13 strategies and returns a report dict mapping
        strategy name → match count.  Useful for diagnostic assertions.

        Returns:
            Dict[str, int]: e.g. {"LINK_TEXT": 0, "ALL_ANCHORS": 0, ...}
        """
        report: Dict[str, int] = {}
        for strategy_name, by, value in self._FORGOT_SELECTORS:
            count = len(self._driver.find_elements(by, value))
            report[strategy_name] = count
            self._logger.debug(f"  [{strategy_name}] → {count}")
        return report

    def is_forgot_password_visible(self) -> bool:
        """
        Convenience method: returns True if any 'Forgot Password' element is
        visible on the page, False if the feature is absent.

        Returns:
            bool: True if element found and displayed, False otherwise.
        """
        element = self.find_forgot_password_element()
        if element is None:
            return False
        try:
            return element.is_displayed()
        except Exception:
            return False

    def click_forgot_password(self) -> None:
        """
        Attempts to click the 'Forgot Password' element.
        Raises AssertionError if the element is not found on the page.
        """
        element = self.find_forgot_password_element()
        if element is None:
            raise AssertionError(
                "Cannot click 'Forgot Password' — element is absent. "
                "Requirement SAUC-7 is NOT implemented in SauceDemo."
            )
        element.click()
        self._logger.info("Clicked 'Forgot Password' element.")

    def get_anchor_tag_count(self) -> int:
        """Returns the total count of <a> (anchor) tags on the login page."""
        count = self.count_elements_by_tag("a")
        self._logger.info(f"Total anchor tags on login page: {count}")
        return count
