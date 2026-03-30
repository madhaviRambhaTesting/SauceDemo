"""
driver_factory.py
-----------------
DriverFactory — creates and configures Chrome / Firefox WebDriver instances.
Interface Segregation: sole responsibility is driver lifecycle creation.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class DriverFactory:
    """
    Factory that produces configured Selenium WebDriver instances.

    Updated for TC-83 (Parameterized Multi-User Login):
    - Supports Chrome and Firefox browsers
    - Headless mode configurable via Config.HEADLESS
    - Window size set to 1920x1080 for consistent test execution
    - Used by conftest.py driver fixture for all 5 valid user scenarios
    """

    @staticmethod
    def get_driver(browser: str = Config.BROWSER,
                   headless: bool = Config.HEADLESS) -> webdriver.Remote:
        """
        Instantiate and return a WebDriver for the requested browser.

        Parameters
        ----------
        browser : str
            Target browser name — ``'chrome'`` (default) or ``'firefox'``.
        headless : bool
            Run without a visible browser window when ``True``.

        Returns
        -------
        selenium.webdriver.Remote
            A fully configured WebDriver instance.

        Raises
        ------
        ValueError
            If an unsupported browser name is supplied.
        """
        browser = browser.lower().strip()
        logger.info(f"Creating '{browser}' driver | headless={headless}")

        if browser == "chrome":
            return DriverFactory._create_chrome(headless)
        elif browser == "firefox":
            return DriverFactory._create_firefox(headless)
        else:
            raise ValueError(
                f"Unsupported browser: '{browser}'. Choose 'chrome' or 'firefox'."
            )

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _create_chrome(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info("Chrome WebDriver created successfully")
        return driver

    @staticmethod
    def _create_firefox(headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={Config.WINDOW_SIZE.split(',')[0]}")
        options.add_argument(f"--height={Config.WINDOW_SIZE.split(',')[1]}")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info("Firefox WebDriver created successfully")
        return driver
