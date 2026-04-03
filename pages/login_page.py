"""
Login Page Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript
QTest ID    : 11194308

Description : Encapsulates all locators and interactions for the SauceDemo
              login page (https://www.saucedemo.com/).  Specifically extends
              BasePage with TC-96 methods that verify (or attempt to exercise)
              the 'Forgot Password' link.

Known behaviour (TC-96 finding)
--------------------------------
The SauceDemo login page does NOT implement a 'Forgot Password' feature.
The DOM contains only:
  • Username input   (#user-name)
  • Password input   (#password)
  • Login button     (#login-button)

All 'Forgot Password' related locators therefore return no elements, which
causes ``is_forgot_password_visible()`` to return ``False`` — the expected
(and documented) failing assertion for this test case.
"""

import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import BasePage
from utils.config import BASE_URL

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object for https://www.saucedemo.com/.

    Locators
    --------
    All locators are defined as class-level tuples so that they can be
    referenced independently of any driver instance (easy to maintain /
    override in subclasses).
    """

    # ------------------------------------------------------------------ #
    #  Standard login-page locators                                        #
    # ------------------------------------------------------------------ #
    _USERNAME_INPUT    = (By.ID, "user-name")
    _PASSWORD_INPUT    = (By.ID, "password")
    _LOGIN_BUTTON      = (By.ID, "login-button")
    _LOGIN_LOGO        = (By.CLASS_NAME, "login_logo")
    _ERROR_MESSAGE     = (By.CSS_SELECTOR, "[data-test='error']")

    # ------------------------------------------------------------------ #
    #  TC-96: 'Forgot Password' candidate locators                         #
    #  (exhaustive search — ALL return empty on saucedemo.com)             #
    # ------------------------------------------------------------------ #
    _FORGOT_PASSWORD_LINK_HREF      = (By.CSS_SELECTOR, "a[href*='forgot']")
    _FORGOT_PASSWORD_LINK_ID        = (By.ID, "forgot-password")
    _FORGOT_PASSWORD_LINK_CLASS     = (By.CLASS_NAME, "forgot-password")
    _FORGOT_PASSWORD_DATA_TEST      = (By.CSS_SELECTOR, "[data-test='forgot-password']")
    _FORGOT_PASSWORD_LINK_TEXT      = (By.LINK_TEXT, "Forgot Password")
    _FORGOT_PASSWORD_PARTIAL_TEXT   = (By.PARTIAL_LINK_TEXT, "Forgot")
    _ALL_ANCHOR_TAGS                = (By.TAG_NAME, "a")

    def __init__(self, driver) -> None:
        super().__init__(driver)

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #

    def load(self) -> "LoginPage":
        """Open the SauceDemo login page and return ``self`` for chaining."""
        self.open(BASE_URL)
        return self

    # ------------------------------------------------------------------ #
    #  Page-state verification                                             #
    # ------------------------------------------------------------------ #

    def is_loaded(self) -> bool:
        """
        Return ``True`` when the login page is fully loaded.

        Checks:
          1. Page title equals 'Swag Labs'
          2. Username input is visible
          3. Password input is visible
          4. Login button is visible
        """
        title_ok    = self.get_title() == "Swag Labs"
        username_ok = self.is_element_visible(self._USERNAME_INPUT)
        password_ok = self.is_element_visible(self._PASSWORD_INPUT)
        button_ok   = self.is_element_visible(self._LOGIN_BUTTON)

        loaded = all([title_ok, username_ok, password_ok, button_ok])
        logger.info(
            "LoginPage.is_loaded() → %s  "
            "(title=%s, username=%s, password=%s, login_btn=%s)",
            loaded, title_ok, username_ok, password_ok, button_ok,
        )
        return loaded

    # ------------------------------------------------------------------ #
    #  TC-96 specific methods                                              #
    # ------------------------------------------------------------------ #

    def is_forgot_password_visible(self) -> bool:
        """
        Return ``True`` if a 'Forgot Password' link/element is **visible**
        on the login page.

        Strategy: try every known locator variant; return ``True`` as soon
        as any match is found and visible.  Logs each attempt for traceability.

        Expected result for saucedemo.com → ``False`` (no such element).
        """
        locators_to_try = [
            ("href*='forgot'",              self._FORGOT_PASSWORD_LINK_HREF),
            ("id='forgot-password'",        self._FORGOT_PASSWORD_LINK_ID),
            ("class='forgot-password'",     self._FORGOT_PASSWORD_LINK_CLASS),
            ("data-test='forgot-password'", self._FORGOT_PASSWORD_DATA_TEST),
            ("link_text='Forgot Password'", self._FORGOT_PASSWORD_LINK_TEXT),
            ("partial_text='Forgot'",       self._FORGOT_PASSWORD_PARTIAL_TEXT),
        ]

        for description, locator in locators_to_try:
            if self.is_element_visible(locator):
                logger.info(
                    "TC-96 ✅ 'Forgot Password' element FOUND via: %s", description
                )
                return True
            logger.debug(
                "TC-96 — locator [%s] returned no visible element", description
            )

        # Final fallback: count all <a> tags on the page
        anchors = self.find_elements(self._ALL_ANCHOR_TAGS)
        logger.info(
            "TC-96 DOM inspection — total <a> tags on login page: %d", len(anchors)
        )
        for anchor in anchors:
            href = anchor.get_attribute("href") or ""
            text = anchor.text or ""
            logger.debug("  <a href='%s'>%s</a>", href, text)
            if "forgot" in href.lower() or "forgot" in text.lower():
                logger.info("TC-96 ✅ 'Forgot' found in anchor — href=%s text=%s", href, text)
                return True

        logger.warning(
            "TC-96 ❌ No 'Forgot Password' element found anywhere in DOM. "
            "Total anchors: %d",
            len(anchors),
        )
        return False

    def click_forgot_password(self) -> None:
        """
        Click the 'Forgot Password' link.

        Raises
        ------
        NoSuchElementException
            When no 'Forgot Password' element is present (expected on
            saucedemo.com — documented as TC-96 FAIL scenario).
        """
        locators_to_try = [
            self._FORGOT_PASSWORD_LINK_HREF,
            self._FORGOT_PASSWORD_LINK_ID,
            self._FORGOT_PASSWORD_LINK_TEXT,
            self._FORGOT_PASSWORD_PARTIAL_TEXT,
            self._FORGOT_PASSWORD_DATA_TEST,
        ]

        for locator in locators_to_try:
            if self.is_element_clickable(locator):
                self.click(locator)
                logger.info("TC-96 — clicked 'Forgot Password' via locator: %s", locator)
                return

        msg = (
            "TC-96 NoSuchElementException: 'Forgot Password' link/button does not "
            "exist on https://www.saucedemo.com/ — the feature is not implemented."
        )
        logger.error(msg)
        raise NoSuchElementException(msg)

    # ------------------------------------------------------------------ #
    #  Standard login helper (kept for completeness / other TCs)          #
    # ------------------------------------------------------------------ #

    def login(self, username: str, password: str) -> None:
        """Enter credentials and submit the login form."""
        self.enter_text(self._USERNAME_INPUT, username)
        self.enter_text(self._PASSWORD_INPUT, password)
        self.click(self._LOGIN_BUTTON)
        logger.info("Login submitted with username='%s'", username)

    def get_error_message(self) -> str:
        """Return the text of the inline error banner (if displayed)."""
        if self.is_element_visible(self._ERROR_MESSAGE):
            return self.get_text(self._ERROR_MESSAGE)
        return ""
