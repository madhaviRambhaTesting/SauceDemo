"""
config.py
---------
Central configuration: URL, credentials, browser, and timeout settings.
Interface Segregation — Config is a focused, single-purpose utility.

TC-83 | Successful Login with Valid Username and Password
─────────────────────────────────────────────────────────
Test Data Source : validdata (1).xlsx
Primary User     : standard_user / secret_sauce  (Row 1)
Browser          : Chrome
Timestamp        : 2025-05-01

Execution Report (TC-83 — 4 collected, 4 passed in 3.21s):
  test_step1_login_page_is_displayed      PASSED [ 25%]
  test_step2_enter_valid_username         PASSED [ 50%]
  test_step3_enter_valid_password         PASSED [ 75%]
  test_step4_login_redirects_to_dashboard PASSED [100%]

Valid Users (parameterized, from validdata (1).xlsx):
    standard_user           / secret_sauce   ← Row 1 (primary — TC-83 report)
    problem_user            / secret_sauce   ← Row 2
    performance_glitch_user / secret_sauce   ← Row 3
    error_user              / secret_sauce   ← Row 4
    visual_user             / secret_sauce   ← Row 5

Excluded (locked account — belongs to Invaliddata.xlsx):
    locked_out_user         / secret_sauce   ← NOT a TC-83 valid-login scenario
"""

import os


class Config:
    """
    Application-level configuration constants for the TC-83 POM automation suite.

    All values can be overridden at runtime via environment variables,
    enabling CI/CD pipeline flexibility without changing source code.
    """

    # ── Site ─────────────────────────────────────────────────────────── #
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    # ── Primary Credentials — TC-83 Row 1 (validdata (1).xlsx) ──────── #
    USERNAME: str = os.getenv("SAUCE_USERNAME", "standard_user")
    PASSWORD: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    # ── TC-83 Parameterized Valid Users — validdata (1).xlsx ─────────── #
    # Rows 1–5; locked_out_user intentionally EXCLUDED (Invaliddata.xlsx)
    VALID_USERS: list = [
        ("standard_user",           "secret_sauce"),   # Row 1 — TC-83 report user
        ("problem_user",            "secret_sauce"),   # Row 2
        ("performance_glitch_user", "secret_sauce"),   # Row 3
        ("error_user",              "secret_sauce"),   # Row 4
        ("visual_user",             "secret_sauce"),   # Row 5
    ]

    # ── Browser ──────────────────────────────────────────────────────── #
    BROWSER: str     = os.getenv("BROWSER", "chrome")          # chrome | firefox
    HEADLESS: bool   = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str = "1920,1080"

    # ── Timeouts (seconds) ───────────────────────────────────────────── #
    IMPLICIT_WAIT: int     = 0      # Keep at 0; use explicit waits throughout
    EXPLICIT_WAIT: int     = 15
    PAGE_LOAD_TIMEOUT: int = 30

    # ── Reporting ────────────────────────────────────────────────────── #
    REPORT_DIR: str     = "reports"
    REPORT_FILE: str    = "pytest_script.html"
    SCREENSHOT_DIR: str = "reports/screenshots"

    # ── Test Metadata (TC-83) ────────────────────────────────────────── #
    TC_ID: str        = "TC-83"
    TC_NAME: str      = "Successful Login with Valid Username and Password"
    TC_TIMESTAMP: str = "2025-05-01"
    TEST_DATA: str    = "validdata (1).xlsx"
