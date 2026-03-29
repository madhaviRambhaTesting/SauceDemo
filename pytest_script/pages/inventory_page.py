"""
inventory_page.py
-----------------
InventoryPage POM — post-login dashboard (Products page).
Extends BasePage (Open/Closed Principle).

TC-83 Step 4 assertion target:
    URL      : https://www.saucedemo.com/inventory.html
    Title    : Products
    Items    : 6 inventory cards
    Cart     : Shopping cart icon visible
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class InventoryPage(BasePage):
    """Page Object for the SauceDemo Inventory / Products page."""

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    _PAGE_TITLE        = (By.CLASS_NAME, "title")
    _INVENTORY_ITEMS   = (By.CLASS_NAME, "inventory_item")
    _CART_ICON         = (By.CLASS_NAME, "shopping_cart_link")
    _APP_LOGO          = (By.CLASS_NAME, "app_logo")
    _BURGER_MENU       = (By.ID, "react-burger-menu-btn")

    # ------------------------------------------------------------------ #
    #  Queries / Validations                                               #
    # ------------------------------------------------------------------ #
    def get_page_header_title(self) -> str:
        """Return the text of the 'Products' header on the inventory page."""
        return self.get_text(self._PAGE_TITLE)

    def get_inventory_item_count(self) -> int:
        """Return the number of product cards displayed."""
        items = self.find_elements(self._INVENTORY_ITEMS)
        count = len(items)
        logger.info(f"Inventory items found: {count}")
        return count

    def is_cart_icon_visible(self) -> bool:
        """Return True if the shopping cart icon is displayed."""
        return self.is_element_visible(self._CART_ICON)

    def is_app_logo_visible(self) -> bool:
        """Return True if the Sauce Labs app logo is visible."""
        return self.is_element_visible(self._APP_LOGO)

    def is_burger_menu_visible(self) -> bool:
        """Return True if the hamburger navigation menu is visible."""
        return self.is_element_visible(self._BURGER_MENU)

    def is_on_inventory_page(self) -> bool:
        """Return True when the current URL contains 'inventory'."""
        return "inventory" in self.get_current_url()
