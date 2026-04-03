"""
dashboard_page.py
-----------------
DashboardPage POM — post-login Products / Inventory dashboard.
Extends BasePage (Open/Closed Principle).

TC-83 | Successful Login with Valid Username and Password
Test Data : validdata (1).xlsx → standard_user / secret_sauce
Timestamp : 2025-05-01

Step 4 Execution Result (from TC-83 report):
    ✔ URL     = inventory.html       → PASSED
    ✔ Title   = 'Products'           → PASSED
    ✔ Items   = 6 product cards      → PASSED
    ✔ Cart    = shopping cart visible → PASSED

Locators:
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    _INVENTORY_CONT  = (By.ID,         "inventory_container")
    _CART_ICON       = (By.CLASS_NAME, "shopping_cart_link")
    _APP_LOGO        = (By.CLASS_NAME, "app_logo")
    _BURGER_MENU     = (By.ID,         "react-burger-menu-btn")
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class DashboardPage(BasePage):
    """
    Page Object for the SauceDemo Products / Dashboard page.

    Used by TC-83 Step 4 assertions:
      ✔ is_loaded()              → URL contains 'inventory' + container visible
      ✔ get_page_title()         → Returns 'Products' header text
      ✔ get_inventory_item_count() → Returns product card count (expected: 6)
      ✔ is_cart_icon_visible()   → Shopping cart link is visible

    TC-83 Execution Report — Step 4 Actual Result:
        URL = inventory.html ✅   Title = 'Products' ✅
    """

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    _PAGE_TITLE        = (By.CLASS_NAME, "title")
    _INVENTORY_ITEMS   = (By.CLASS_NAME, "inventory_item")
    _INVENTORY_CONT    = (By.ID, "inventory_container")
    _CART_ICON         = (By.CLASS_NAME, "shopping_cart_link")
    _APP_LOGO          = (By.CLASS_NAME, "app_logo")
    _BURGER_MENU       = (By.ID, "react-burger-menu-btn")

    # Expected values (TC-83 Step 4 assertions)
    EXPECTED_URL_FRAGMENT = "inventory"
    EXPECTED_PAGE_TITLE   = "Products"
    EXPECTED_ITEM_COUNT   = 6

    # ------------------------------------------------------------------ #
    #  Load Verification — TC-83 Step 4 primary assertion                #
    # ------------------------------------------------------------------ #
    def is_loaded(self) -> bool:
        """
        Return True when the Products dashboard is fully loaded.

        TC-83 Step 4 assertion:
            assert dashboard.is_loaded()

        Checks:
          1. Current URL contains 'inventory'
          2. Inventory container element is visible in DOM
        """
        url_ok      = self.EXPECTED_URL_FRAGMENT in self.get_current_url()
        container   = self.is_element_visible(self._INVENTORY_CONT)
        result      = url_ok and container
        logger.info(
            f"[DashboardPage] is_loaded → "
            f"url_ok={url_ok}, container_visible={container} → {result}"
        )
        return result

    def is_dashboard_loaded(self) -> bool:
        """
        Composite assertion: URL + title + items — all three conditions met.

        Returns True only when:
          ✔ URL contains 'inventory'
          ✔ Page title text == 'Products'
          ✔ At least one inventory item is visible
        """
        url_ok   = self.EXPECTED_URL_FRAGMENT in self.get_current_url()
        title_ok = self.get_page_header_title() == self.EXPECTED_PAGE_TITLE
        items_ok = self.is_element_visible(self._INVENTORY_ITEMS)
        logger.info(
            f"[DashboardPage] is_dashboard_loaded → "
            f"URL={url_ok}, Title={title_ok}, Items={items_ok}"
        )
        return url_ok and title_ok and items_ok

    # ------------------------------------------------------------------ #
    #  TC-83 Step 4 Individual Assertion Methods                          #
    # ------------------------------------------------------------------ #
    def get_page_title(self) -> str:
        """
        Return the 'Products' page header text.

        TC-83 Step 4 assertion:
            assert dashboard.get_page_title().lower() == 'products'
        """
        title = self.get_text(self._PAGE_TITLE)
        logger.info(f"[DashboardPage] Page header title: '{title}'")
        return title

    def get_page_header_title(self) -> str:
        """Alias for get_page_title() — returns 'Products' header text."""
        return self.get_text(self._PAGE_TITLE)

    def get_inventory_item_count(self) -> int:
        """
        Return the number of product cards rendered on the dashboard.

        TC-83 Step 4 assertion:
            assert dashboard.get_inventory_item_count() == 6
        """
        items = self.find_elements(self._INVENTORY_ITEMS)
        count = len(items)
        logger.info(f"[DashboardPage] Inventory item count: {count}")
        return count

    def is_cart_icon_visible(self) -> bool:
        """
        Return True if the shopping cart icon/link is visible.

        TC-83 Step 4 assertion:
            assert dashboard.is_cart_icon_visible()
        """
        visible = self.is_element_visible(self._CART_ICON)
        logger.info(f"[DashboardPage] Cart icon visible: {visible}")
        return visible

    def is_app_logo_visible(self) -> bool:
        """Return True if the Sauce Labs app logo is visible on the dashboard."""
        return self.is_element_visible(self._APP_LOGO)

    def is_burger_menu_visible(self) -> bool:
        """Return True if the hamburger/navigation menu button is visible."""
        return self.is_element_visible(self._BURGER_MENU)

    def is_on_inventory_page(self) -> bool:
        """Return True if the current URL targets /inventory.html."""
        return self.EXPECTED_URL_FRAGMENT in self.get_current_url()
