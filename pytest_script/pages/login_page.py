"""
login_page.py
-------------
TC-83 | Successful Login with Valid Username and Password
LoginPage POM — locators + login actions for https://www.saucedemo.com/
Extends BasePage (Open/Closed Principle).

Steps Covered:
  Step 1: Navigate to https://www.saucedemo.com/ → login page loads
  Step 2: Enter username 'standard_user' into id=user-name
  Step 3: Enter password 'secret_sauce' (type=password, masked)
  Step 4: Click Login button → redirected to inventory.html
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID = "TC-83"


class LoginPage(BasePage):
    """
    Page Object for the SauceDemo login screen.
    TC-83 | Successful Login with Valid Username and Password
    URL: https://www.saucedemo.com/
    """

    # ------------------------------------------------------------------ #
    #  Locators  (Step 1 — all three must be visible on page load)        #
    # ------------------------------------------------------------------ #
    _USERNAME_INPUT = (By.ID, "user-name")        # Step 2 target
    _PASSWORD_INPUT = (By.ID, "password")          # Step 3 target
    _LOGIN_BUTTON   = (By.ID, "login-button")      # Step 4 trigger
    _ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")
    _LOGIN_LOGO     = (By.CLASS_NAME, "login_logo")

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #
    def enter_username(self, username: str) -> None:
        """TC-83 Step 2: Type the username into id=user-name field."""
        logger.info(f"[{TC_ID}] Step 2 — Entering username: '{username}' into id=user-name")
        self.type_text(self._USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """TC-83 Step 3: Type the password into id=password field (type=password, masked)."""
        logger.info(f"[{TC_ID}] Step 3 — Entering password: [MASKED] into id=password")
        self.type_text(self._PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """TC-83 Step 4: Click the Login button (id=login-button)."""
        logger.info(f"[{TC_ID}] Step 4 — Clicking Login button (id=login-button)")
        self.click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """TC-83 Steps 2–4 combined: enter credentials and submit login form."""
        logger.info(f"[{TC_ID}] Executing full login: Steps 2→3→4")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ------------------------------------------------------------------ #
    #  Queries / Validations  (Step 1 assertions)                         #
    # ------------------------------------------------------------------ #
    def is_username_field_visible(self) -> bool:
        """TC-83 Step 1: Verify id=user-name is visible on login page."""
        return self.is_element_visible(self._USERNAME_INPUT)

    def is_password_field_visible(self) -> bool:
        """TC-83 Step 1: Verify id=password is visible on login page."""
        return self.is_element_visible(self._PASSWORD_INPUT)

    def is_login_button_visible(self) -> bool:
        """TC-83 Step 1: Verify id=login-button is visible on login page."""
        return self.is_element_visible(self._LOGIN_BUTTON)

    def get_username_value(self) -> str:
        """TC-83 Step 2: Return typed value of the username field."""
        return self.get_attribute(self._USERNAME_INPUT, "value")

    def get_password_value(self) -> str:
        """TC-83 Step 3: Return typed value of the password field."""
        return self.get_attribute(self._PASSWORD_INPUT, "value")

    def get_password_field_type(self) -> str:
        """TC-83 Step 3: Return 'type' attribute — must equal 'password' (masked)."""
        return self.get_attribute(self._PASSWORD_INPUT, "type")

    def get_error_message(self) -> str:
        """Return the login error message text if displayed."""
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if a login error banner is visible (should be False for TC-83)."""
        return self.is_element_visible(self._ERROR_MESSAGE)
