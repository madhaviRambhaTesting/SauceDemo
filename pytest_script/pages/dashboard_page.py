"""
dashboard_page.py
-----------------
DashboardPage POM — alias / wrapper for InventoryPage post-login assertions.
Extends BasePage (Open/Closed Principle).

Used by TC-83 Step 4 to confirm successful login redirect:
    assert dashboard.is_dashboard_loaded()
    → URL contains 'inventory.html', title == 'Products', items == 6
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class DashboardPage(BasePage):
    """
    Page Object for the SauceDemo Products / Dashboard page.
    Provides high-level post-login assertions for TC-83.
    """

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    _CART_ICON       = (By.CLASS_NAME, "shopping_cart_link")
    _APP_LOGO        = (By.CLASS_NAME, "app_logo")
    _BURGER_MENU     = (By.ID, "react-burger-menu-btn")

    # ------------------------------------------------------------------ #
    #  High-level validation                                               #
    # ------------------------------------------------------------------ #
    def is_dashboard_loaded(self) -> bool:
        """
        Composite assertion used by TC-83 Step 4:
          ✔ URL contains '/inventory.html'
          ✔ Inventory list is visible
          ✔ Page title equals 'Products'

        Returns True only when all three conditions are satisfied.
        """
        url_ok    = "inventory" in self.get_current_url()
        title_ok  = self.get_page_header_title() == "Products"
        items_ok  = self.is_element_visible(self._INVENTORY_ITEMS)

        logger.info(
            f"[DashboardPage] is_dashboard_loaded → "
            f"URL={url_ok}, Title={title_ok}, Items={items_ok}"
        )
        return url_ok and title_ok and items_ok

    # ------------------------------------------------------------------ #
    #  Individual queries                                                  #
    # ------------------------------------------------------------------ #
    def get_page_header_title(self) -> str:
        """Return the 'Products' header text."""
        return self.get_text(self._PAGE_TITLE)

    def get_inventory_item_count(self) -> int:
        """Return the number of product cards on the dashboard."""
        items = self.find_elements(self._INVENTORY_ITEMS)
        count = len(items)
        logger.info(f"Dashboard inventory items found: {count}")
        return count

    def is_cart_icon_visible(self) -> bool:
        """Return True if the shopping cart icon is visible."""
        return self.is_element_visible(self._CART_ICON)

    def is_on_inventory_page(self) -> bool:
        """Return True if the current URL targets /inventory.html."""
        return "inventory" in self.get_current_url()
