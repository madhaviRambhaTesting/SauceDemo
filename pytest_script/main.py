# main.py — Entry point to run TC-83 pytest suite

import subprocess
import sys
import os


def main():
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(os.path.join(report_dir, "screenshots"), exist_ok=True)

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_tc83_login.py",
            "-v",
            "--tb=short",
            "--html=reports/pytest_script.html",
            "--self-contained-html",
            "--log-cli-level=INFO",
        ],
        cwd=os.path.dirname(__file__)
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
