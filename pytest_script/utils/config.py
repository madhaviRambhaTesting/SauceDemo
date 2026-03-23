"""
config.py
---------
Central configuration: URL, credentials, browser, and timeout settings.
Interface Segregation — Config is a focused, single-purpose utility.
"""

import os


class Config:
    """Application-level configuration constants."""

    # ── Site ─────────────────────────────────────────────────────────── #
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    # ── Credentials ──────────────────────────────────────────────────── #
    USERNAME: str = os.getenv("SAUCE_USERNAME", "standard_user")
    PASSWORD: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    # ── Browser ──────────────────────────────────────────────────────── #
    BROWSER: str       = os.getenv("BROWSER", "chrome")   # chrome | firefox
    HEADLESS: bool     = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str   = "1920,1080"

    # ── Timeouts (seconds) ───────────────────────────────────────────── #
    IMPLICIT_WAIT: int  = 0     # Use explicit waits; keep implicit at 0
    EXPLICIT_WAIT: int  = 10
    PAGE_LOAD_TIMEOUT: int = 30

    # ── Reporting ────────────────────────────────────────────────────── #
    REPORT_DIR: str  = "reports"
    REPORT_FILE: str = "pytest_script.html"

    # ── Test metadata ────────────────────────────────────────────────── #
    TC_ID: str   = "TC-83"
    TC_NAME: str = "Successful Login with Valid Username and Password"
