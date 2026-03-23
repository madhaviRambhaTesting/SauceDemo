"""
login_page.py
-------------
LoginPage POM — locators + login actions for https://www.saucedemo.com/
Extends BasePage (Open/Closed Principle).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class LoginPage(BasePage):
    """Page Object for the SauceDemo login screen."""

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    _USERNAME_INPUT    = (By.ID, "user-name")
    _PASSWORD_INPUT    = (By.ID, "password")
    _LOGIN_BUTTON      = (By.ID, "login-button")
    _ERROR_MESSAGE     = (By.CSS_SELECTOR, "[data-test='error']")
    _LOGIN_LOGO        = (By.CLASS_NAME, "login_logo")

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #
    def enter_username(self, username: str) -> None:
        """Type the username into the username input field."""
        logger.info(f"Entering username: {username}")
        self.type_text(self._USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Type the password into the password input field."""
        logger.info("Entering password: [MASKED]")
        self.type_text(self._PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Click the Login button."""
        logger.info("Clicking Login button")
        self.click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Convenience method: enter credentials and click Login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ------------------------------------------------------------------ #
    #  Queries / Validations                                               #
    # ------------------------------------------------------------------ #
    def is_username_field_visible(self) -> bool:
        return self.is_element_visible(self._USERNAME_INPUT)

    def is_password_field_visible(self) -> bool:
        return self.is_element_visible(self._PASSWORD_INPUT)

    def is_login_button_visible(self) -> bool:
        return self.is_element_visible(self._LOGIN_BUTTON)

    def get_username_value(self) -> str:
        """Return the current value of the username input."""
        return self.get_attribute(self._USERNAME_INPUT, "value")

    def get_password_value(self) -> str:
        """Return the current value of the password input."""
        return self.get_attribute(self._PASSWORD_INPUT, "value")

    def get_password_field_type(self) -> str:
        """Return the 'type' attribute of the password field (should be 'password')."""
        return self.get_attribute(self._PASSWORD_INPUT, "type")

    def get_error_message(self) -> str:
        """Return the login error message text, if displayed."""
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if a login error message is shown."""
        return self.is_element_visible(self._ERROR_MESSAGE)
