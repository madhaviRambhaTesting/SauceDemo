"""
config.py
---------
Central configuration: URL, credentials, browser, and timeout settings.
Interface Segregation — Config is a focused, single-purpose utility.

TC-83  |  Successful Login with Valid Username and Password
QTest ID: 11194292  |  Priority: High
URL: https://www.saucedemo.com/
"""

import os


class Config:
    """Application-level configuration constants."""

    # ── Site ─────────────────────────────────────────────────────────── #
    BASE_URL: str      = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    INVENTORY_URL: str = os.getenv("INVENTORY_URL", "https://www.saucedemo.com/inventory.html")

    # ── Credentials ──────────────────────────────────────────────────── #
    USERNAME: str = os.getenv("SAUCE_USERNAME", "standard_user")
    PASSWORD: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    # ── Browser ──────────────────────────────────────────────────────── #
    BROWSER: str       = os.getenv("BROWSER", "chrome")   # chrome | firefox
    HEADLESS: bool     = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str   = "1920,1080"

    # ── Timeouts (seconds) ───────────────────────────────────────────── #
    IMPLICIT_WAIT: int     = 0     # Use explicit waits; keep implicit at 0
    EXPLICIT_WAIT: int     = 10
    PAGE_LOAD_TIMEOUT: int = 30

    # ── Reporting ────────────────────────────────────────────────────── #
    REPORT_DIR: str  = "reports"
    REPORT_FILE: str = "pytest_script.html"

    # ── Test metadata ────────────────────────────────────────────────── #
    TC_ID: str    = "TC-83"
    TC_NAME: str  = "Successful Login with Valid Username and Password"
    QTEST_ID: str = "11194292"
    PRIORITY: str = "High"
