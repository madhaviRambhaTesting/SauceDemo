"""
config.py
---------
TC-83 | Successful Login with Valid Username and Password
Central configuration: URL, credentials, browser, and timeout settings.
SOLID: Interface Segregation — Config is a focused, single-purpose utility.

Environment Variables Supported:
  BASE_URL        — Override target URL (default: https://www.saucedemo.com/)
  SAUCE_USERNAME  — Override test username (default: standard_user)
  SAUCE_PASSWORD  — Override test password (default: secret_sauce)
  BROWSER         — Target browser: chrome | firefox (default: chrome)
  HEADLESS        — Run headless: true | false (default: true)
"""

import os


class Config:
    """
    TC-83 Application-level configuration constants.
    All values overridable via environment variables for CI/CD pipelines.
    """

    # ── Site ─────────────────────────────────────────────────────────── #
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    # ── TC-83 Credentials ────────────────────────────────────────────── #
    USERNAME: str = os.getenv("SAUCE_USERNAME", "standard_user")   # TC-83 Step 2
    PASSWORD: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")    # TC-83 Step 3

    # ── Browser ──────────────────────────────────────────────────────── #
    BROWSER: str     = os.getenv("BROWSER", "chrome")              # chrome | firefox
    HEADLESS: bool   = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str = "1920,1080"

    # ── Timeouts (seconds) ───────────────────────────────────────────── #
    IMPLICIT_WAIT: int    = 0       # Explicit waits preferred; keep at 0
    EXPLICIT_WAIT: int    = 10
    PAGE_LOAD_TIMEOUT: int = 30

    # ── Reporting ────────────────────────────────────────────────────── #
    REPORT_DIR: str  = "reports"
    REPORT_FILE: str = "pytest_script.html"
    REPORT_TITLE: str = "TC-83 | Successful Login — SauceDemo Test Report"

    # ── TC-83 Metadata ───────────────────────────────────────────────── #
    TC_ID: str      = "TC-83"
    TC_NAME: str    = "Successful Login with Valid Username and Password"
    TC_PRIORITY: str = "High"
    TC_STATUS: str  = "New"
    TC_LINK: str    = "SAUC-3 — User Login with Username and Password"

    # ── TC-83 Expected Results ───────────────────────────────────────── #
    EXPECTED_HEADER: str      = "Products"
    EXPECTED_ITEM_COUNT: int  = 6
    EXPECTED_URL_FRAGMENT: str = "inventory.html"
    EXPECTED_PASSWORD_TYPE: str = "password"
