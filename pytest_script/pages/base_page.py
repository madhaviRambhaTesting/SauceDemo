"""
base_page.py
------------
BasePage: Reusable WebDriver interactions following Single Responsibility Principle.
All page objects extend this class (Open/Closed + Liskov Substitution).
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class BasePage:
    """Base class for all Page Objects. Encapsulates common WebDriver interactions."""

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(driver, timeout=10)

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #
    def open(self, url: str) -> None:
        """Navigate to the given URL."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the page <title> text."""
        return self.driver.title

    # ------------------------------------------------------------------ #
    #  Element interactions                                                #
    # ------------------------------------------------------------------ #
    def find_element(self, locator: tuple):
        """Wait for visibility and return a single web element."""
        try:
            element = self._wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found (timeout): {locator}")
            raise

    def find_elements(self, locator: tuple) -> list:
        """Return all matching elements (no wait for each)."""
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple) -> None:
        """Click a web element after waiting for it to be clickable."""
        element = self._wait.until(EC.element_to_be_clickable(locator))
        logger.info(f"Clicking element: {locator}")
        element.click()

    def type_text(self, locator: tuple, text: str) -> None:
        """Clear a field and type the given text."""
        element = self.find_element(locator)
        element.clear()
        logger.info(f"Typing '{text}' into: {locator}")
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        return self.find_element(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Return the value of the given attribute of an element."""
        return self.find_element(locator).get_attribute(attribute)

    def is_element_visible(self, locator: tuple) -> bool:
        """Return True if the element is visible on the page."""
        try:
            self._wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Return True if the element exists in the DOM (not necessarily visible)."""
        try:
            self._wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
