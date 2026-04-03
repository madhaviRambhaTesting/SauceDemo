# pages/login_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage(BasePage):
    """Page Object Model for the SauceDemo Login page."""

    # ── Locators ──────────────────────────────────────────────────────────────
    USERNAME_INPUT   = (By.ID, "user-name")
    PASSWORD_INPUT   = (By.ID, "password")
    LOGIN_BUTTON     = (By.ID, "login-button")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_LOGO       = (By.CLASS_NAME, "login_logo")

    # ── Actions ───────────────────────────────────────────────────────────────
    def is_login_page_displayed(self) -> bool:
        """Verify all critical login-page elements are visible."""
        logger.info("Verifying login page elements are visible.")
        return (
            self.is_element_visible(*self.USERNAME_INPUT) and
            self.is_element_visible(*self.PASSWORD_INPUT) and
            self.is_element_visible(*self.LOGIN_BUTTON)
        )

    def enter_username(self, username: str):
        logger.info(f"Entering username: {username}")
        self.type_text(*self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        logger.info("Entering password: [MASKED]")
        self.type_text(*self.PASSWORD_INPUT, password)

    def is_password_masked(self) -> bool:
        """Confirm password field type is 'password' (masked)."""
        attr = self.get_attribute(*self.PASSWORD_INPUT, "type")
        logger.info(f"Password input type: {attr}")
        return attr == "password"

    def click_login(self):
        logger.info("Clicking Login button.")
        self.click(*self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_MESSAGE)

    def login(self, username: str, password: str):
        """High-level login action combining all login steps."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
