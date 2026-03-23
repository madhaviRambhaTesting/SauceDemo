"""
main.py
-------
TC-83 | Successful Login with Valid Username and Password
Entry point: runs the complete TC-83 test suite via pytest and generates
a self-contained HTML report at reports/pytest_script.html.

Usage:
    python main.py                    # Run all TC-83 tests
    python main.py --smoke            # Run only @pytest.mark.smoke
    python main.py --headed           # Run with visible browser

Test Matrix Covered:
    test_tc83_login_page_displayed              → Step 1
    test_tc83_enter_username                    → Step 2
    test_tc83_enter_password                    → Step 3
    test_tc83_successful_login_redirects_to_inv → Step 4
    test_tc83_login_no_error_on_valid_creds     → Bonus
    test_tc83_full_login_flow [smoke]           → Steps 1–4 E2E
"""

import os
import sys
import pytest
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

SEPARATOR = "=" * 70


def main() -> int:
    """
    Run TC-83 pytest suite programmatically.

    Returns
    -------
    int
        pytest exit code (0 = all passed, 1 = some failed).
    """
    # Ensure output directories exist
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    report_path = os.path.join(Config.REPORT_DIR, Config.REPORT_FILE)

    logger.info(SEPARATOR)
    logger.info(f"  TC-83 Test Suite — {Config.TC_NAME}")
    logger.info(f"  Priority  : {Config.TC_PRIORITY}")
    logger.info(f"  Linked    : {Config.TC_LINK}")
    logger.info(f"  Target URL: {Config.BASE_URL}")
    logger.info(f"  Browser   : {Config.BROWSER} (headless={Config.HEADLESS})")
    logger.info(f"  Report    : {report_path}")
    logger.info(f"  Log file  : logs/tc83_test_run.log")
    logger.info(SEPARATOR)

    # Parse optional CLI overrides
    smoke_only = "--smoke"  in sys.argv
    headed     = "--headed" in sys.argv

    if headed:
        os.environ["HEADLESS"] = "false"
        logger.info("  Mode: HEADED (visible browser)")

    args = [
        "tests/test_tc83_login.py",
        "-v",
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        "--capture=sys",
    ]

    if smoke_only:
        args += ["-m", "smoke"]
        logger.info("  Filter: @pytest.mark.smoke only")

    logger.info(SEPARATOR)
    logger.info("  ▶ Starting test execution...")
    logger.info(SEPARATOR)

    exit_code = pytest.main(args)

    logger.info(SEPARATOR)
    if exit_code == 0:
        logger.info(f"  ✅ ALL TESTS PASSED — TC-83 verified successfully")
    else:
        logger.warning(f"  ❌ SOME TESTS FAILED — exit code: {exit_code}")
    logger.info(f"  📊 HTML Report : {report_path}")
    logger.info(f"  📝 Log File    : logs/tc83_test_run.log")
    logger.info(SEPARATOR)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
