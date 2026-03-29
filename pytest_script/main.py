"""
main.py
-------
Entry point: discovers and runs the TC-83 test suite,
then generates a self-contained HTML report at reports/pytest_script.html.

TC-83: Successful Login with Valid Username and Password
URL  : https://www.saucedemo.com/
Creds: standard_user / secret_sauce (from validdata.xlsx)
"""

import os
import sys
import pytest
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


def main() -> int:
    """Run pytest programmatically and return the exit code."""

    # Ensure the reports directory exists
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    report_path = os.path.join(Config.REPORT_DIR, Config.REPORT_FILE)

    logger.info("=" * 60)
    logger.info(f"  Starting test suite: {Config.TC_ID} — {Config.TC_NAME}")
    logger.info(f"  Target URL  : {Config.BASE_URL}")
    logger.info(f"  Username    : {Config.USERNAME}  (from validdata.xlsx)")
    logger.info(f"  Browser     : {Config.BROWSER} (headless={Config.HEADLESS})")
    logger.info(f"  Report      : {report_path}")
    logger.info("=" * 60)

    args = [
        "tests/test_tc83_login.py",      # Test module
        "-v",                            # Verbose output
        "--tb=short",                    # Short traceback on failure
        f"--html={report_path}",         # HTML report path
        "--self-contained-html",         # Single-file report (no external assets)
        "--capture=sys",                 # Capture stdout/stderr per test
    ]

    exit_code = pytest.main(args)

    if exit_code == 0:
        logger.info(f"✅  All tests PASSED — Report: {report_path}")
    else:
        logger.warning(f"❌  Some tests FAILED (exit code {exit_code}) — Report: {report_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
