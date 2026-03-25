"""
base_test.py
------------
BaseTest — shared setup / teardown lifecycle for all test classes.
Manages WebDriver instantiation and teardown (Single Responsibility).
"""

# tests/base_test.py — TC-83 | SauceDemo Login Automation Suite
import pytest
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class BaseTest:
    """
    Parent class for all test classes.
    Provides `driver`, `login_page`, and `inventory_page` via pytest fixtures
    defined in conftest.py. Direct instantiation of pages is handled here
    so individual test classes stay clean.
    """

    @pytest.fixture(autouse=True)
    def setup_teardown(self, driver):
        """
        Receive the `driver` fixture from conftest, store it on self,
        and guarantee browser teardown after each test.
        """
        self.driver = driver
        logger.info(f"[Setup] Browser ready | Test: {self.__class__.__name__}")
        yield
        logger.info(f"[Teardown] Closing browser | Test: {self.__class__.__name__}")
        # Driver quit is handled in conftest fixture; no double-quit needed.
