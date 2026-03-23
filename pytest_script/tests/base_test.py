"""
base_test.py
------------
TC-83 | Successful Login with Valid Username and Password
BaseTest — shared setup / teardown lifecycle for all test classes.
Single Responsibility: manages only WebDriver lifecycle for tests.
Dependency Inversion: depends on DriverFactory abstraction.
"""

import pytest
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID = "TC-83"


class BaseTest:
    """
    Parent class for all TC-83 test classes.
    Provides `driver` fixture integration via conftest.py.
    Implements: Single Responsibility + Dependency Inversion (SOLID).

    Note: WebDriver is created and destroyed per test function
    via conftest.py `driver` fixture (function scope).
    """

    @pytest.fixture(autouse=True)
    def setup_teardown(self, driver):
        """
        TC-83: Receive the `driver` fixture from conftest.py,
        store it on `self`, then yield control to the test.
        Driver quit is handled exclusively in conftest.py — no double-quit.
        """
        self.driver = driver
        logger.info(
            f"[{TC_ID}] [Setup] Browser ready → "
            f"Test: {self.__class__.__name__} | "
            f"Browser: {Config.BROWSER} (headless={Config.HEADLESS})"
        )
        yield
        logger.info(
            f"[{TC_ID}] [Teardown] Test complete → "
            f"{self.__class__.__name__} | Driver quit via conftest"
        )
