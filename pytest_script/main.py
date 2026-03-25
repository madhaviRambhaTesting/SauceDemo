# main.py — TC-83 | SauceDemo Login Automation Suite

"""
Entry point for the TC-83 Pytest automation suite.
Executes all TC-83 tests and generates an HTML report at:
    reports/pytest_script.html
"""

import subprocess
import sys
import os
from utils.logger import get_logger

logger = get_logger("main")


def main():
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    logger.info("Starting TC-83 Pytest execution via main.py ...")

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_login_page.py",
            "-v",
            "--tb=short",
            "--html=reports/pytest_script.html",
            "--self-contained-html",
            "-m", "tc83",
        ],
        capture_output=False,
    )

    logger.info(f"Pytest finished with exit code: {result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
