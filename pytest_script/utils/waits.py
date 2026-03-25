"""
waits.py
--------
WaitHelper — explicit wait utilities built on top of Selenium WebDriverWait.
Interface Segregation: a standalone, driver-agnostic wait utility.
"""

# utils/waits.py — TC-83 | SauceDemo Login Automation Suite
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class WaitHelper:
    """
    Provides explicit-wait methods to complement BasePage interactions.
    Instantiate with a WebDriver instance; all timeouts default to Config.EXPLICIT_WAIT.
    """

    def __init__(self, driver, timeout: int = Config.EXPLICIT_WAIT):
        self._driver  = driver
        self._timeout = timeout
        self._wait    = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------ #
    #  Presence / Visibility                                               #
    # ------------------------------------------------------------------ #
    def wait_for_element_visible(self, locator: tuple):
        """Wait until the element is visible; return the element."""
        logger.debug(f"Waiting for element to be visible: {locator}")
        return self._wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_present(self, locator: tuple):
        """Wait until the element is present in the DOM; return the element."""
        logger.debug(f"Waiting for element to be present: {locator}")
        return self._wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple):
        """Wait until the element is clickable; return the element."""
        logger.debug(f"Waiting for element to be clickable: {locator}")
        return self._wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_invisible(self, locator: tuple) -> bool:
        """Wait until the element is no longer visible; return True on success."""
        logger.debug(f"Waiting for element to be invisible: {locator}")
        return self._wait.until(EC.invisibility_of_element_located(locator))

    # ------------------------------------------------------------------ #
    #  URL / Title                                                         #
    # ------------------------------------------------------------------ #
    def wait_for_url_to_contain(self, fragment: str) -> bool:
        """Wait until the current URL contains the given fragment."""
        logger.debug(f"Waiting for URL to contain: '{fragment}'")
        return self._wait.until(EC.url_contains(fragment))

    def wait_for_title_to_contain(self, title_fragment: str) -> bool:
        """Wait until the page title contains the given string."""
        logger.debug(f"Waiting for title to contain: '{title_fragment}'")
        return self._wait.until(EC.title_contains(title_fragment))

    # ------------------------------------------------------------------ #
    #  Safe checks (return bool, no exception)                             #
    # ------------------------------------------------------------------ #
    def is_element_visible_after_wait(self, locator: tuple) -> bool:
        """Return True if visible within timeout, False otherwise."""
        try:
            self.wait_for_element_visible(locator)
            return True
        except TimeoutException:
            logger.warning(f"Element not visible after {self._timeout}s: {locator}")
            return False

    def is_url_containing_after_wait(self, fragment: str) -> bool:
        """Return True if URL contains fragment within timeout, False otherwise."""
        try:
            return self.wait_for_url_to_contain(fragment)
        except TimeoutException:
            logger.warning(f"URL did not contain '{fragment}' after {self._timeout}s")
            return False
