# utils/wait_helper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.config import EXPLICIT_WAIT


class WaitHelper:
    """Centralized explicit wait utilities."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def until_visible(self, by: By, locator: str):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def until_clickable(self, by: By, locator: str):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def until_url_contains(self, partial_url: str):
        return self.wait.until(EC.url_contains(partial_url))

    def until_element_present(self, by: By, locator: str):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
