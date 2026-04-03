# utils/config.py

import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
