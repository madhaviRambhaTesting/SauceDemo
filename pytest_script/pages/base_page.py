# pages/base_page.py

import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils.wait_helper import WaitHelper
from utils.config import SCREENSHOT_DIR
from utils.logger import get_logger

logger = get_logger("BasePage")


class BasePage:
    """Base class for all Page Object Models — centralizes common interactions."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait_helper = WaitHelper(driver)

    # ── Navigation ──────────────────────────────────────────────────────────
    def navigate_to(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ── Element Retrieval ────────────────────────────────────────────────────
    def find_element(self, by: By, locator: str):
        return self.wait_helper.until_visible(by, locator)

    def find_clickable(self, by: By, locator: str):
        return self.wait_helper.until_clickable(by, locator)

    # ── Interactions ─────────────────────────────────────────────────────────
    def click(self, by: By, locator: str):
        element = self.find_clickable(by, locator)
        logger.info(f"Clicking element: [{by}] {locator}")
        element.click()

    def type_text(self, by: By, locator: str, text: str):
        element = self.find_element(by, locator)
        element.clear()
        logger.info(f"Typing '{text}' into element: [{by}] {locator}")
        element.send_keys(text)

    def get_text(self, by: By, locator: str) -> str:
        element = self.find_element(by, locator)
        return element.text.strip()

    def get_attribute(self, by: By, locator: str, attr: str) -> str:
        element = self.find_element(by, locator)
        return element.get_attribute(attr)

    def is_element_visible(self, by: By, locator: str) -> bool:
        try:
            element = self.wait_helper.until_visible(by, locator)
            return element.is_displayed()
        except Exception:
            return False

    # ── Screenshot ───────────────────────────────────────────────────────────
    def take_screenshot(self, test_name: str) -> str:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath

    # ── Assertion Helpers ────────────────────────────────────────────────────
    def assert_url_contains(self, partial_url: str):
        self.wait_helper.until_url_contains(partial_url)
        current = self.get_current_url()
        assert partial_url in current, (
            f"Expected URL to contain '{partial_url}', got '{current}'"
        )
        logger.info(f"URL assertion passed: '{partial_url}' found in '{current}'")
