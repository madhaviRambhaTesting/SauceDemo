"""
Configuration Module — TC-96: Forgot Password Link Visibility
Repository  : madhaviRambhaTesting/SauceDemo
Branch      : qtestidscript

Description : Single source of truth for all environment-level settings.
              Values can be overridden via environment variables so the same
              suite can run locally or in CI without code changes.
"""

import os

# ---------------------------------------------------------------------------
# Application under test
# ---------------------------------------------------------------------------
BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")

# ---------------------------------------------------------------------------
# Browser / driver configuration
# ---------------------------------------------------------------------------
BROWSER: str  = os.getenv("BROWSER", "chrome")
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")

WINDOW_WIDTH:  int = int(os.getenv("WINDOW_WIDTH",  "1920"))
WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "1080"))

# ---------------------------------------------------------------------------
# Wait / timeout settings (seconds)
# ---------------------------------------------------------------------------
DEFAULT_TIMEOUT:   int   = int(os.getenv("DEFAULT_TIMEOUT",   "10"))
IMPLICIT_WAIT:     int   = int(os.getenv("IMPLICIT_WAIT",     "0"))   # 0 = explicit-wait only
PAGE_LOAD_TIMEOUT: int   = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
POLL_FREQUENCY:    float = float(os.getenv("POLL_FREQUENCY",  "0.5"))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT_DIR:       str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR:     str = os.path.join(_ROOT_DIR, "reports")
SCREENSHOTS_DIR: str = os.path.join(REPORTS_DIR, "screenshots")
LOG_DIR:         str = os.path.join(_ROOT_DIR, "logs")
HTML_REPORT_PATH:str = os.path.join(REPORTS_DIR, "pytest_script.html")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE:  str = os.path.join(LOG_DIR, "test_execution.log")

# ---------------------------------------------------------------------------
# Test credentials (SauceDemo standard users)
# ---------------------------------------------------------------------------
STANDARD_USER:   str = os.getenv("SAUCE_USER",     "standard_user")
STANDARD_PASS:   str = os.getenv("SAUCE_PASSWORD",  "secret_sauce")
LOCKED_OUT_USER: str = os.getenv("SAUCE_LOCKED_USER", "locked_out_user")
