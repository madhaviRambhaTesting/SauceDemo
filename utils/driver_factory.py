"""
utils/driver_factory.py — WebDriver factory using the Page-Object Model convention.

Supported browsers
------------------
* chrome  (default) — managed via webdriver-manager
* firefox            — managed via webdriver-manager

The active browser is controlled by ``utils.config.BROWSER``.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import BROWSER
from utils.logger import get_logger

logger = get_logger(__name__)


def get_driver() -> webdriver.Remote:
    """
    Instantiate and return a Selenium WebDriver for the configured browser.

    Returns
    -------
    webdriver.Remote
        A fully initialised, maximised browser session.

    Raises
    ------
    ValueError
        If ``BROWSER`` is set to an unsupported value.
    """
    browser = BROWSER.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        driver.maximize_window()

    else:
        raise ValueError(
            f"Unsupported browser: '{browser}'. "
            "Set BROWSER to 'chrome' or 'firefox' in utils/config.py"
        )

    logger.info(f"Browser '{browser}' launched and maximised.")
    return driver
