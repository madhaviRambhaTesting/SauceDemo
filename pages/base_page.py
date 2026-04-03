"""
base_page.py
------------
Abstract base class for all Page Object Model (POM) pages.
Follows OCP and DRY — shared reusable methods for all page classes.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
URL: https://www.saucedemo.com/
"""

import os
from datetime import datetime
from typing import Tuple, Optional, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.wait_helper import WaitHelper
from utils.logger import get_logger


class BasePage:
    """
    Base class for all Page Objects.
    Provides reusable element interaction and screenshot utilities.
    All page classes must inherit from this class.
    """

    BASE_URL: str = "https://www.saucedemo.com/"

    def __init__(self, driver: WebDriver):
        """
        Initialises the BasePage with a WebDriver instance.

        Args:
            driver (WebDriver): Active Selenium WebDriver instance.
        """
        self._driver = driver
        self._wait = WaitHelper(driver)
        self._logger = get_logger(self.__class__.__name__)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self, url: str = BASE_URL) -> None:
        """Navigates to the specified URL."""
        self._logger.info(f"Navigating to: {url}")
        self._driver.get(url)

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self._driver.current_url

    def get_page_title(self) -> str:
        """Returns the current page title."""
        return self._driver.title

    # ── Element Interactions ──────────────────────────────────────────────────

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Finds and returns a single element by locator after waiting for visibility.

        Args:
            locator (Tuple[str, str]): (By, value) locator tuple.

        Returns:
            WebElement: The located element.
        """
        self._logger.debug(f"Finding element: {locator}")
        return self._wait.wait_for_element_visible(locator)

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Returns a list of matching elements (may be empty).

        Args:
            locator (Tuple[str, str]): (By, value) locator tuple.

        Returns:
            List[WebElement]: Matching elements list, possibly empty.
        """
        self._logger.debug(f"Finding elements: {locator}")
        return self._driver.find_elements(*locator)

    def click(self, locator: Tuple[str, str]) -> None:
        """Waits for element to be clickable, then clicks it."""
        self._logger.debug(f"Clicking element: {locator}")
        element = self._wait.wait_for_element_clickable(locator)
        element.click()

    def enter_text(self, locator: Tuple[str, str], text: str) -> None:
        """Clears the field and enters the provided text."""
        self._logger.debug(f"Entering text '{text}' into: {locator}")
        element = self._wait.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """Returns the visible text content of an element."""
        element = self._wait.wait_for_element_visible(locator)
        return element.text

    # ── Presence Checks ───────────────────────────────────────────────────────

    def is_element_present(
        self, locator: Tuple[str, str], timeout: int = 5
    ) -> bool:
        """
        Non-throwing check for element presence.

        Args:
            locator (Tuple[str, str]): (By, value) locator tuple.
            timeout (int): Seconds to wait before returning False.

        Returns:
            bool: True if element found, False otherwise.
        """
        return self._wait.is_element_present(locator, timeout)

    def is_element_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Checks if an element is present AND displayed/visible.

        Args:
            locator (Tuple[str, str]): (By, value) locator tuple.

        Returns:
            bool: True if element is visible, False otherwise.
        """
        try:
            element = self._driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    # ── Screenshot Utility ────────────────────────────────────────────────────

    def take_screenshot(self, test_name: str, status: str = "FAIL") -> str:
        """
        Captures a screenshot and saves it to reports/screenshots/.

        Args:
            test_name (str): Name of the test for the filename.
            status (str): Status label (PASS/FAIL). Defaults to 'FAIL'.

        Returns:
            str: Absolute path to the saved screenshot file.
        """
        screenshots_dir = os.path.join(
            os.path.dirname(__file__), "..", "reports", "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        self._driver.save_screenshot(filepath)
        self._logger.info(f"Screenshot saved: {filepath}")
        return filepath

    # ── Page Source Helpers ───────────────────────────────────────────────────

    def get_page_source(self) -> str:
        """Returns the full page source HTML."""
        return self._driver.page_source

    def count_elements_by_tag(self, tag_name: str) -> int:
        """
        Counts all elements on the page matching the given HTML tag.

        Args:
            tag_name (str): HTML tag name, e.g. 'a', 'button', 'input'.

        Returns:
            int: Count of matching elements.
        """
        elements = self._driver.find_elements(By.TAG_NAME, tag_name)
        return len(elements)
