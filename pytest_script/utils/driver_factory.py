# utils/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for WebDriver instantiation."""

    @staticmethod
    def get_driver(browser: str = "chrome", headless: bool = False):
        browser = browser.lower()
        logger.info(f"Launching browser: {browser} | Headless: {headless}")

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.maximize_window()
        logger.info("Browser launched and maximized.")
        return driver
