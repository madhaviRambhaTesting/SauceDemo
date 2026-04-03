"""
Driver Factory Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript

Description : Centralises WebDriver creation so tests never manage driver
              options directly.  Supports Chrome (default) and Firefox via
              the BROWSER environment variable or direct method arguments.

Usage
-----
.. code-block:: python

    driver = DriverFactory.create_driver()          # Chrome headless
    driver = DriverFactory.create_driver("firefox") # Firefox headless
"""

import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    _WDM_AVAILABLE = True
except ImportError:
    _WDM_AVAILABLE = False

from utils.config import (
    BROWSER,
    HEADLESS,
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)

logger = logging.getLogger(__name__)


class DriverFactory:
    """
    Factory class for Selenium WebDriver instances.

    All driver-creation logic lives here, keeping test code driver-agnostic.
    """

    @staticmethod
    def create_driver(browser: str | None = None) -> webdriver.Remote:
        """
        Create and return a configured WebDriver.

        Parameters
        ----------
        browser : str, optional
            ``'chrome'`` (default) or ``'firefox'``.
            Falls back to the ``BROWSER`` config value, then to ``'chrome'``.

        Returns
        -------
        selenium.webdriver.Remote
            A fully configured, ready-to-use WebDriver instance.

        Raises
        ------
        ValueError
            If an unsupported browser name is provided.
        """
        target_browser = (browser or BROWSER).lower().strip()
        logger.info("Creating %s WebDriver (headless=%s)", target_browser, HEADLESS)

        if target_browser in ("chrome", "chromium"):
            driver = DriverFactory._chrome_driver()
        elif target_browser in ("firefox", "gecko"):
            driver = DriverFactory._firefox_driver()
        else:
            raise ValueError(
                f"Unsupported browser: '{target_browser}'. "
                "Choose 'chrome' or 'firefox'."
            )

        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        logger.info(
            "WebDriver ready — browser=%s | window=%dx%d",
            target_browser, WINDOW_WIDTH, WINDOW_HEIGHT,
        )
        return driver

    # ------------------------------------------------------------------
    # Private: per-browser builders
    # ------------------------------------------------------------------

    @staticmethod
    def _chrome_driver() -> webdriver.Chrome:
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if _WDM_AVAILABLE:
            service = ChromeService(ChromeDriverManager().install())
        else:
            service = ChromeService()  # relies on chromedriver being in PATH

        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _firefox_driver() -> webdriver.Firefox:
        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")

        if _WDM_AVAILABLE:
            service = FirefoxService(GeckoDriverManager().install())
        else:
            service = FirefoxService()  # relies on geckodriver being in PATH

        return webdriver.Firefox(service=service, options=options)
