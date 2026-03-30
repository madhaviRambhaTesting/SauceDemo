"""
config.py
---------
Central configuration: URL, credentials, browser, and timeout settings.
Interface Segregation — Config is a focused, single-purpose utility.

TC-83 Credentials (sourced from validdata.xlsx):
    Valid Users (parameterized):
        standard_user          / secret_sauce
        problem_user           / secret_sauce
        performance_glitch_user/ secret_sauce
        error_user             / secret_sauce
        visual_user            / secret_sauce

    Excluded (locked account — not a valid login scenario):
        locked_out_user        / secret_sauce  ← from Invaliddata.xlsx
"""

import os


class Config:
    """Application-level configuration constants."""

    # ── Site ─────────────────────────────────────────────────────────── #
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    # ── Default Credentials (single-user fallback) ───────────────────── #
    USERNAME: str = os.getenv("SAUCE_USERNAME", "standard_user")
    PASSWORD: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    # ── TC-83 Parameterized Valid Users (from validdata.xlsx) ────────── #
    # NOTE: locked_out_user is intentionally EXCLUDED (Invaliddata.xlsx)
    VALID_USERS: list = [
        ("standard_user",           "secret_sauce"),
        ("problem_user",            "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
        ("error_user",              "secret_sauce"),
        ("visual_user",             "secret_sauce"),
    ]

    # ── Browser ──────────────────────────────────────────────────────── #
    BROWSER: str       = os.getenv("BROWSER", "chrome")   # chrome | firefox
    HEADLESS: bool     = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str   = "1920,1080"

    # ── Timeouts (seconds) ───────────────────────────────────────────── #
    IMPLICIT_WAIT: int     = 0     # Use explicit waits; keep implicit at 0
    EXPLICIT_WAIT: int     = 15
    PAGE_LOAD_TIMEOUT: int = 30

    # ── Reporting ────────────────────────────────────────────────────── #
    REPORT_DIR: str        = "reports"
    REPORT_FILE: str       = "pytest_script.html"
    SCREENSHOT_DIR: str    = "reports/screenshots"

    # ── Test metadata ────────────────────────────────────────────────── #
    TC_ID: str   = "TC-83"
    TC_NAME: str = "Successful Login with Valid Username and Password"
