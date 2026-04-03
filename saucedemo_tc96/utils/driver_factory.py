# =============================================================================
# utils/driver_factory.py
# -----------------------------------------------------------------------------
# Responsibility : Single Responsibility — creates and tears down WebDriver.
# Design         : Factory pattern; decoupled from tests and pages.
# Compliance     : SOLID — OCP (new browsers added without changing callers),
#                  DIP (tests depend on abstraction, not concrete driver calls).
# =============================================================================

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class DriverFactory:
    """
    Factory class responsible ONLY for WebDriver creation and disposal.

    Supports Chrome (default) and Firefox.
    Uses webdriver-manager to auto-download matching driver binaries —
    no manual chromedriver management required.

    Usage:
        driver = DriverFactory.create_driver("chrome")
        ...
        DriverFactory.quit_driver(driver)
    """

    SUPPORTED_BROWSERS = ("chrome", "firefox")

    @staticmethod
    def create_driver(browser: str = "chrome") -> webdriver.Remote:
        """
        Instantiate and return a maximised WebDriver for the given browser.

        Args:
            browser (str): Target browser — 'chrome' (default) or 'firefox'.

        Returns:
            webdriver.Remote: Fully initialised, maximised WebDriver instance.

        Raises:
            ValueError: If an unsupported browser name is provided.
        """
        browser = browser.strip().lower()

        if browser not in DriverFactory.SUPPORTED_BROWSERS:
            raise ValueError(
                f"Unsupported browser: '{browser}'. "
                f"Choose from: {DriverFactory.SUPPORTED_BROWSERS}"
            )

        logger.info("DriverFactory → creating '%s' WebDriver …", browser)

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            # Suppress DevTools / USB noise in logs
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--disable-notifications")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service = ChromeService(ChromeDriverManager().install())
            driver  = webdriver.Chrome(service=service, options=options)

        else:  # firefox
            options = FirefoxOptions()
            options.add_argument("--start-maximized")
            service = FirefoxService(GeckoDriverManager().install())
            driver  = webdriver.Firefox(service=service, options=options)

        driver.maximize_window()
        logger.info("DriverFactory → '%s' WebDriver ready.", browser)
        return driver

    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """
        Safely quit and clean up the given WebDriver instance.

        Args:
            driver (webdriver.Remote): The driver to dispose.
        """
        if driver:
            try:
                logger.info("DriverFactory → quitting WebDriver …")
                driver.quit()
                logger.info("DriverFactory → WebDriver session closed.")
            except Exception as exc:  # pragma: no cover
                logger.warning(
                    "DriverFactory → quit() raised an exception (ignored): %s", exc
                )
