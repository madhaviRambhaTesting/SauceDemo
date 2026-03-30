"""
main.py — Entry point to execute TC-83 Pytest suite.

Usage:
    python main.py

Runs the full TC-83 login test suite and generates an HTML report
at reports/pytest_script.html.
"""
import subprocess
import sys


if __name__ == "__main__":
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/test_tc83_login.py", "-v",
            "--html=reports/pytest_script.html", "--self-contained-html",
        ],
        capture_output=False,
    )
    sys.exit(result.returncode)
