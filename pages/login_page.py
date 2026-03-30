"""
pages/login_page.py — Page Object for the SauceDemo login page.

URL : https://www.saucedemo.com/

Locators are defined as class-level tuples so they are never scattered
across test files, keeping the framework maintainable and DRY.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Encapsulates all interactions with the SauceDemo login page.

    Inherits generic driver helpers from BasePage and exposes
    high-level, intent-revealing methods for use in test cases.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")
    APP_LOGO       = (By.CLASS_NAME, "app_logo")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("LoginPage initialised.")

    # ── Page-state queries ────────────────────────────────────────────────────

    def is_login_page_displayed(self) -> bool:
        """
        Return True when all three primary login elements are visible:
        username field, password field, and Login button.
        """
        return (
            self.is_element_visible(self.USERNAME_FIELD)
            and self.is_element_visible(self.PASSWORD_FIELD)
            and self.is_element_visible(self.LOGIN_BUTTON)
        )

    def is_dashboard_displayed(self) -> bool:
        """Return True when the post-login app logo is visible (dashboard loaded)."""
        return self.is_element_visible(self.APP_LOGO)

    def get_error_message(self) -> str:
        """Return the text of the inline error banner shown on failed login."""
        return self.get_text(self.ERROR_MESSAGE)

    # ── User actions ──────────────────────────────────────────────────────────

    def enter_username(self, username: str):
        """Type *username* into the username field."""
        self.type_text(self.USERNAME_FIELD, username)

    def enter_password(self, password: str):
        """Type *password* into the password field."""
        self.type_text(self.PASSWORD_FIELD, password)

    def click_login(self):
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """
        Convenience method: enter credentials and submit the login form.

        Parameters
        ----------
        username : str
        password : str
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.logger.info(f"Login attempted with username='{username}'")
