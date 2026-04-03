"""
driver_factory.py
-----------------
Responsible for creating and configuring the Selenium WebDriver instance.
Follows the Single Responsibility Principle (SRP) — only manages driver lifecycle.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
URL: https://www.saucedemo.com/
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    """
    Factory class to create Selenium WebDriver instances.
    Supports headless and headed Chrome browser modes.
    """

    @staticmethod
    def get_driver(headless: bool = False) -> webdriver.Chrome:
        """
        Creates and returns a configured Chrome WebDriver instance.

        Args:
            headless (bool): If True, runs Chrome in headless mode (no UI).
                             Defaults to False for visual debugging.

        Returns:
            webdriver.Chrome: Fully configured Chrome WebDriver.
        """
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        # Standard options for stability in CI/CD and local environments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(5)

        return driver
