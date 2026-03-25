# pages/base_page.py — TC-83 | SauceDemo Login Automation Suite

import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from utils.config import Config
from utils.logger import get_logger
from utils.waits import WaitHelper

logger = get_logger("BasePage")


class BasePage:
    """
    Base class for all Page Object Models.
    Provides reusable methods for element interactions, navigation,
    screenshots, and assertions — eliminating code duplication across POMs.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitHelper(driver)
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self, url: str = None):
        target = url or Config.BASE_URL
        logger.info(f"Navigating to: {target}")
        self.driver.get(target)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_title(self) -> str:
        return self.driver.title

    # ── Element Finders ────────────────────────────────────────────────────────

    def find_element(self, locator: tuple):
        logger.debug(f"Finding element: {locator}")
        return self.wait.wait_for_element_visible(locator)

    def find_clickable(self, locator: tuple):
        logger.debug(f"Finding clickable element: {locator}")
        return self.wait.wait_for_element_clickable(locator)

    # ── Actions ────────────────────────────────────────────────────────────────

    def click(self, locator: tuple):
        element = self.find_clickable(locator)
        logger.info(f"Clicking element: {locator}")
        element.click()

    def enter_text(self, locator: tuple, text: str):
        element = self.find_element(locator)
        element.clear()
        logger.info(f"Entering text '{text}' into: {locator}")
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        element = self.find_element(locator)
        text = element.text
        logger.debug(f"Got text '{text}' from: {locator}")
        return text

    def is_element_displayed(self, locator: tuple) -> bool:
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    # ── Screenshot ─────────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(Config.SCREENSHOTS_DIR, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_url_contains(self, partial_url: str):
        self.wait.wait_for_url_contains(partial_url)
        assert partial_url in self.get_current_url(), (
            f"Expected URL to contain '{partial_url}', got '{self.get_current_url()}'"
        )

    def assert_element_visible(self, locator: tuple, message: str = ""):
        assert self.is_element_displayed(locator), (
            message or f"Element {locator} is not visible on the page."
        )
