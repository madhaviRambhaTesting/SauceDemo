"""
Base Page Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript
Description : Provides reusable, generic Selenium interactions shared by all
              Page-Object-Model (POM) page classes.  Follows SOLID / DRY
              principles so each concrete page only implements what is unique
              to that page.
"""

import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from utils.config import DEFAULT_TIMEOUT, POLL_FREQUENCY

logger = logging.getLogger(__name__)


class BasePage:
    """
    Abstract base class for all Page Object Model pages.

    Attributes
    ----------
    driver : WebDriver
        The active Selenium WebDriver instance.
    wait : WebDriverWait
        A pre-configured explicit-wait helper.
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver, timeout=timeout, poll_frequency=POLL_FREQUENCY
        )
        logger.debug("BasePage initialised — %s", self.__class__.__name__)

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def open(self, url: str) -> None:
        """Navigate to an absolute URL."""
        logger.info("Navigating to: %s", url)
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the page <title>."""
        return self.driver.title

    # ------------------------------------------------------------------
    # Element retrieval (with explicit wait)
    # ------------------------------------------------------------------

    def find_element(self, locator: tuple) -> WebElement:
        """
        Wait for *locator* to be present in the DOM, then return it.

        Parameters
        ----------
        locator : tuple
            A ``(By.<strategy>, value)`` tuple, e.g.
            ``(By.ID, "login-button")``.

        Raises
        ------
        TimeoutException
            If the element is not found within the configured timeout.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.debug("Element found: %s", locator)
            return element
        except TimeoutException:
            logger.error("Element NOT found within timeout: %s", locator)
            raise

    def find_elements(self, locator: tuple) -> list:
        """
        Return *all* matching elements (may be an empty list).

        Uses ``presence_of_all_elements_located``; returns ``[]`` on
        timeout rather than raising.
        """
        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            logger.debug("Found %d element(s) for: %s", len(elements), locator)
            return elements
        except TimeoutException:
            logger.warning("No elements found for locator: %s", locator)
            return []

    def is_element_present(self, locator: tuple) -> bool:
        """
        Return ``True`` if at least one element matching *locator* exists
        in the DOM **right now** (no wait).
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator: tuple) -> bool:
        """
        Return ``True`` if the element matching *locator* is both present
        and **visible** within the configured timeout.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator: tuple) -> bool:
        """
        Return ``True`` if the element matching *locator* is clickable
        within the configured timeout.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------
    # Interaction helpers
    # ------------------------------------------------------------------

    def click(self, locator: tuple) -> None:
        """Wait until *locator* is clickable, then click it."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info("Clicked element: %s", locator)
        except (TimeoutException, ElementNotInteractableException) as exc:
            logger.error("Could not click element %s — %s", locator, exc)
            raise

    def enter_text(self, locator: tuple, text: str) -> None:
        """Clear the input field and type *text* into it."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.debug("Entered text into %s", locator)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        return self.find_element(locator).text

    # ------------------------------------------------------------------
    # Screenshot helper
    # ------------------------------------------------------------------

    def take_screenshot(self, filepath: str) -> None:
        """Save a PNG screenshot to *filepath*."""
        self.driver.save_screenshot(filepath)
        logger.info("Screenshot saved: %s", filepath)
