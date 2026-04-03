# =============================================================================
# pages/base_page.py
# -----------------------------------------------------------------------------
# Responsibility : Abstract base for ALL Page Object classes.
# Design         : Template Method pattern — defines the common page API that
#                  concrete pages extend without repeating driver boilerplate.
# Compliance     : SOLID
#   SRP  → only handles driver-level interactions (wait, click, screenshot …)
#   OCP  → subclasses extend behaviour without modifying this class
#   LSP  → any BasePage subclass can be substituted wherever BasePage is typed
#   DIP  → depends on WebDriver abstraction, not a concrete browser class
# =============================================================================

import logging
import os
from datetime import datetime
from pathlib import Path

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
DEFAULT_TIMEOUT    = 10   # seconds — explicit wait ceiling
SCREENSHOT_DIR     = Path("reports/screenshots")


class BasePage:
    """
    Abstract superclass for all Page Object classes.

    Every POM inherits:
      • _wait()            — returns a pre-configured WebDriverWait
      • is_visible()       — True / False visibility check (no throw)
      • find()             — waits for & returns a visible WebElement
      • click()            — waits for clickability, then clicks
      • get_text()         — safe inner-text retrieval
      • get_current_url()  — delegate to driver
      • take_screenshot()  — saves PNG to reports/screenshots/
      • navigate_to()      — driver.get() with logging
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Args:
            driver  (WebDriver): Active Selenium WebDriver session.
            timeout (int)      : Global explicit-wait ceiling in seconds.
        """
        self._driver  : WebDriver = driver
        self._timeout : int       = timeout
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug("%s initialised (timeout=%ds)", self.__class__.__name__, timeout)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _wait(self, timeout=None) -> WebDriverWait:
        """Return a WebDriverWait bound to this page's driver & timeout."""
        return WebDriverWait(self._driver, timeout or self._timeout)

    # ── Element retrieval ─────────────────────────────────────────────────────

    def find(self, locator: tuple, timeout=None) -> WebElement:
        """
        Wait until *locator* is visible in the DOM, then return it.

        Args:
            locator (tuple): (By.XX, "selector") e.g. (By.ID, "user-name")
            timeout (int)  : Override the page-level timeout for this call.

        Returns:
            WebElement: The first matching visible element.

        Raises:
            TimeoutException: If element is not visible within *timeout*.
        """
        try:
            element = self._wait(timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug("find() → located %s", locator)
            return element
        except TimeoutException:
            logger.error("find() TIMEOUT → locator %s not visible after %ds",
                         locator, timeout or self._timeout)
            raise

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Non-throwing visibility probe — returns True/False.

        Uses a short timeout so failed probes don't slow the suite.

        Args:
            locator (tuple): (By.XX, "selector")
            timeout (int)  : Max seconds to wait (default: 5).

        Returns:
            bool: True if element becomes visible within *timeout*.
        """
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            logger.debug("is_visible() → True for %s", locator)
            return True
        except (TimeoutException, NoSuchElementException):
            logger.debug("is_visible() → False for %s", locator)
            return False

    def is_present(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Check DOM presence (element may be hidden / off-screen).

        Args:
            locator (tuple): (By.XX, "selector")
            timeout (int)  : Max seconds to wait (default: 5).

        Returns:
            bool: True if element is present in DOM within *timeout*.
        """
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            logger.debug("is_present() → True for %s", locator)
            return True
        except (TimeoutException, NoSuchElementException):
            logger.debug("is_present() → False for %s", locator)
            return False

    def count_elements(self, locator: tuple) -> int:
        """
        Return the number of elements currently matching *locator* in the DOM.

        Args:
            locator (tuple): (By.XX, "selector")

        Returns:
            int: Element count (0 if none found).
        """
        elements = self._driver.find_elements(*locator)
        count = len(elements)
        logger.debug("count_elements() → %d elements for %s", count, locator)
        return count

    # ── Interactions ──────────────────────────────────────────────────────────

    def click(self, locator: tuple, timeout=None) -> None:
        """
        Wait until *locator* is clickable, then perform a click.

        Args:
            locator (tuple): (By.XX, "selector")
            timeout (int)  : Override page-level timeout for this call.

        Raises:
            TimeoutException            : Element not clickable in time.
            ElementNotInteractableException : Element present but blocked.
        """
        try:
            element = self._wait(timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info("click() → clicked %s", locator)
        except TimeoutException:
            logger.error("click() TIMEOUT → %s not clickable after %ds",
                         locator, timeout or self._timeout)
            raise
        except ElementNotInteractableException:
            logger.error("click() BLOCKED → %s is present but not interactable", locator)
            raise

    def get_text(self, locator: tuple, timeout=None) -> str:
        """
        Return the visible inner text of the element matched by *locator*.

        Args:
            locator (tuple): (By.XX, "selector")
            timeout (int)  : Override page-level timeout.

        Returns:
            str: Stripped inner text (empty string if element has no text).
        """
        element = self.find(locator, timeout)
        text = element.text.strip()
        logger.debug("get_text() → '%s' from %s", text, locator)
        return text

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate_to(self, url: str) -> None:
        """
        Direct the browser to *url* and log the action.

        Args:
            url (str): Fully qualified URL string.
        """
        logger.info("navigate_to() → %s", url)
        self._driver.get(url)

    def get_current_url(self) -> str:
        """Return the browser's current URL string."""
        url = self._driver.current_url
        logger.debug("get_current_url() → %s", url)
        return url

    def get_page_source(self) -> str:
        """Return the full page HTML source."""
        return self._driver.page_source

    # ── Screenshot ────────────────────────────────────────────────────────────

    def take_screenshot(self, filename: str) -> str:
        """
        Capture a PNG screenshot and save it to reports/screenshots/.

        Args:
            filename (str): Desired file name WITHOUT extension
                            e.g. "TC96_Step2_ForgotPwd_NOT_FOUND_failure"

        Returns:
            str: Absolute path to the saved screenshot file.
        """
        # Sanitise filename — replace spaces/colons with underscores
        safe_name = filename.replace(" ", "_").replace(":", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_name = f"{safe_name}_{timestamp}.png"
        filepath  = SCREENSHOT_DIR / full_name

        self._driver.save_screenshot(str(filepath))
        logger.info("Screenshot saved → %s", filepath)
        return str(filepath)
