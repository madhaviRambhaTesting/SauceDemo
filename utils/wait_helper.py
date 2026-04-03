"""
wait_helper.py
--------------
Provides explicit WebDriverWait strategies to avoid flaky tests caused by
timing issues.  Follows SRP — only responsible for wait operations.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from typing import Tuple


class WaitHelper:
    """
    Encapsulates Selenium explicit wait strategies for reliable element interaction.
    """

    DEFAULT_TIMEOUT: int = 15

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialises WaitHelper with a WebDriver and a default timeout.

        Args:
            driver (WebDriver): Active Selenium WebDriver instance.
            timeout (int): Maximum seconds to wait. Defaults to 15.
        """
        self._driver = driver
        self._timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    # ── Visibility Waits ──────────────────────────────────────────────────────

    def wait_for_element_visible(self, locator: Tuple[str, str]) -> WebElement:
        """Waits until the element identified by *locator* is visible."""
        return self._wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible after {self._timeout}s — locator: {locator}",
        )

    def wait_for_element_present(self, locator: Tuple[str, str]) -> WebElement:
        """Waits until the element is present in the DOM (may not be visible)."""
        return self._wait.until(
            EC.presence_of_element_located(locator),
            message=f"Element not present after {self._timeout}s — locator: {locator}",
        )

    def wait_for_element_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """Waits until the element is clickable."""
        return self._wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable after {self._timeout}s — locator: {locator}",
        )

    # ── URL / Title Waits ─────────────────────────────────────────────────────

    def wait_for_url_contains(self, partial_url: str) -> bool:
        """Waits until the current URL contains *partial_url*."""
        return self._wait.until(
            EC.url_contains(partial_url),
            message=f"URL did not contain '{partial_url}' after {self._timeout}s",
        )

    def wait_for_title_contains(self, partial_title: str) -> bool:
        """Waits until the page title contains *partial_title*."""
        return self._wait.until(
            EC.title_contains(partial_title),
            message=f"Title did not contain '{partial_title}' after {self._timeout}s",
        )

    # ── Absence Waits ─────────────────────────────────────────────────────────

    def wait_for_element_invisible(self, locator: Tuple[str, str]) -> bool:
        """Waits until the element identified by *locator* is no longer visible."""
        return self._wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"Element still visible after {self._timeout}s — locator: {locator}",
        )

    # ── Safe Check ────────────────────────────────────────────────────────────

    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Non-throwing check — returns True if element appears within *timeout* seconds.

        Args:
            locator (Tuple[str, str]): Selenium (By, value) locator tuple.
            timeout (int): Override timeout for this check. Defaults to 5.

        Returns:
            bool: True if element is found, False otherwise.
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
