"""
utils/config.py — Central configuration for the test framework.

All tuneable parameters (URL, browser, waits, paths) live here so that
no magic strings are scattered through page objects or test files.
"""

# ── Application Under Test ───────────────────────────────────────────────────
BASE_URL: str = "https://www.saucedemo.com/"

# ── Browser configuration ────────────────────────────────────────────────────
BROWSER: str = "chrome"          # Options: "chrome" | "firefox"

# ── Wait timeouts (seconds) ──────────────────────────────────────────────────
IMPLICIT_WAIT: int = 10
EXPLICIT_WAIT: int = 15

# ── Reporting & artefacts ────────────────────────────────────────────────────
SCREENSHOT_DIR: str = "reports/screenshots"
