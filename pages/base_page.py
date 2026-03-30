"""
pages/base_page.py — Abstract base class for all Page Objects.

Provides reusable, explicit-wait-backed helpers so that concrete page
classes stay thin and focus only on page-specific locators / actions.

Design principles applied
--------------------------
* Single Responsibility  — only generic driver interactions live here.
* Open/Closed            — extend BasePage; don't modify it for new pages.
* Liskov Substitution    — every Page Object IS-A BasePage.
* Dependency Inversion   — depends on WebDriver abstraction, not concrete driver.
"""
import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.config import EXPLICIT_WAIT, SCREENSHOT_DIR
from utils.logger import get_logger


class BasePage:
    """Base class inherited by every page object in this framework."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)

    # ── Core interactions ────────────────────────────────────────────────────

    def find_element(self, locator):
        """Wait for element presence and return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Wait for element to be clickable, then click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        self.logger.info(f"Clicked element: {locator}")

    def type_text(self, locator, text: str):
        """Clear the field and type the supplied text."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Typed '{text}' into element: {locator}")

    def get_text(self, locator) -> str:
        """Return the visible text of the first matching element."""
        return self.find_element(locator).text

    # ── Visibility helpers ───────────────────────────────────────────────────

    def is_element_visible(self, locator) -> bool:
        """Return True if the element becomes visible within the explicit wait."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ── Navigation helpers ───────────────────────────────────────────────────

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    # ── Reporting helpers ────────────────────────────────────────────────────

    def take_screenshot(self, test_name: str) -> str:
        """
        Capture a PNG screenshot and save it under SCREENSHOT_DIR.

        Parameters
        ----------
        test_name : str
            Used as part of the filename so screenshots are easy to identify.

        Returns
        -------
        str
            Absolute path to the saved screenshot file.
        """
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOT_DIR}/{test_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved: {filename}")
        return filename
