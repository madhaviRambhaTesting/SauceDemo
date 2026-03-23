"""
driver_factory.py
-----------------
TC-83 | Successful Login with Valid Username and Password
DriverFactory — creates and configures Chrome / Firefox WebDriver instances.
SOLID: Dependency Inversion — tests depend on this abstraction, not on WebDriver directly.
       Interface Segregation — sole responsibility: WebDriver creation.
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

TC_ID = "TC-83"


class DriverFactory:
    """
    Factory that produces configured Selenium WebDriver instances.
    TC-83: Supports Chrome (default) and Firefox browsers.
    Implements Dependency Inversion — all TC-83 tests depend on this factory.
    """

    @staticmethod
    def get_driver(
        browser: str = Config.BROWSER,
        headless: bool = Config.HEADLESS,
    ) -> webdriver.Remote:
        """
        Instantiate and return a WebDriver for the requested browser.

        Parameters
        ----------
        browser : str
            Target browser — 'chrome' (default) or 'firefox'.
        headless : bool
            Run without a visible window when True (CI/CD compatible).

        Returns
        -------
        selenium.webdriver.Remote
            Fully configured WebDriver with page-load timeout set.

        Raises
        ------
        ValueError
            If an unsupported browser name is supplied.
        """
        browser = browser.lower().strip()
        logger.info(
            f"[{TC_ID}] DriverFactory → creating '{browser}' driver "
            f"| headless={headless} | window={Config.WINDOW_SIZE}"
        )

        if browser == "chrome":
            return DriverFactory._create_chrome(headless)
        elif browser == "firefox":
            return DriverFactory._create_firefox(headless)
        else:
            raise ValueError(
                f"[{TC_ID}] Unsupported browser: '{browser}'. "
                f"Supported: 'chrome', 'firefox'."
            )

    # ------------------------------------------------------------------ #
    #  Private factory helpers                                             #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _create_chrome(headless: bool) -> webdriver.Chrome:
        """Create and return a configured Chrome WebDriver instance."""
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info(f"[{TC_ID}] ✅ Chrome WebDriver ready (headless={headless})")
        return driver

    @staticmethod
    def _create_firefox(headless: bool) -> webdriver.Firefox:
        """Create and return a configured Firefox WebDriver instance."""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        w, h = Config.WINDOW_SIZE.split(",")
        options.add_argument(f"--width={w}")
        options.add_argument(f"--height={h}")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info(f"[{TC_ID}] ✅ Firefox WebDriver ready (headless={headless})")
        return driver
