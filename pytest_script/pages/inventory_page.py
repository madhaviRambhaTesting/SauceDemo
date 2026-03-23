"""
inventory_page.py
-----------------
TC-83 | Successful Login with Valid Username and Password
InventoryPage POM — post-login dashboard (Products page).
Extends BasePage (Open/Closed Principle).

Step 4 Assertions:
  ✅ URL contains 'inventory.html'
  ✅ Page header text == 'Products'
  ✅ 6 inventory items rendered
  ✅ Shopping cart icon visible
  ✅ No error banner displayed
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

TC_ID = "TC-83"
EXPECTED_ITEM_COUNT = 6
EXPECTED_HEADER = "Products"


class InventoryPage(BasePage):
    """
    Page Object for the SauceDemo Inventory / Products page.
    TC-83 Step 4 — post-login verification after successful login.
    URL pattern: https://www.saucedemo.com/inventory.html
    """

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    _PAGE_TITLE      = (By.CLASS_NAME, "title")           # 'Products' header
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")  # 6 product cards
    _CART_ICON       = (By.CLASS_NAME, "shopping_cart_link")
    _APP_LOGO        = (By.CLASS_NAME, "app_logo")
    _BURGER_MENU     = (By.ID, "react-burger-menu-btn")

    # ------------------------------------------------------------------ #
    #  TC-83 Step 4 — Post-Login Assertions                               #
    # ------------------------------------------------------------------ #
    def get_page_header_title(self) -> str:
        """
        TC-83 Step 4: Return the Products page header text.
        Expected: 'Products'
        """
        header = self.get_text(self._PAGE_TITLE)
        logger.info(f"[{TC_ID}] Step 4 — Page header: '{header}' (expected: '{EXPECTED_HEADER}')")
        return header

    def get_inventory_item_count(self) -> int:
        """
        TC-83 Step 4: Return the number of product cards on the page.
        Expected: 6
        """
        items = self.find_elements(self._INVENTORY_ITEMS)
        count = len(items)
        logger.info(f"[{TC_ID}] Step 4 — Inventory items: {count} (expected: {EXPECTED_ITEM_COUNT})")
        return count

    def is_cart_icon_visible(self) -> bool:
        """TC-83 Step 4: Return True if the shopping cart icon is displayed."""
        visible = self.is_element_visible(self._CART_ICON)
        logger.info(f"[{TC_ID}] Step 4 — Cart icon visible: {visible}")
        return visible

    def is_app_logo_visible(self) -> bool:
        """Return True if the Sauce Labs app logo is visible."""
        return self.is_element_visible(self._APP_LOGO)

    def is_burger_menu_visible(self) -> bool:
        """Return True if the hamburger navigation menu is visible."""
        return self.is_element_visible(self._BURGER_MENU)

    def is_on_inventory_page(self) -> bool:
        """
        TC-83 Step 4: Return True when the current URL contains 'inventory'.
        Confirms successful redirect after login.
        """
        current_url = self.get_current_url()
        on_page = "inventory" in current_url
        logger.info(f"[{TC_ID}] Step 4 — On inventory page: {on_page} | URL: {current_url}")
        return on_page

    def assert_inventory_page_loaded(self) -> None:
        """
        TC-83 Step 4 compound assertion helper.
        Verifies URL, header, item count, and cart icon in a single call.
        """
        assert self.is_on_inventory_page(), \
            f"[{TC_ID}] Step 4 FAIL: Not on inventory page. URL={self.get_current_url()}"
        assert self.get_page_header_title() == EXPECTED_HEADER, \
            f"[{TC_ID}] Step 4 FAIL: Header != '{EXPECTED_HEADER}'"
        assert self.get_inventory_item_count() == EXPECTED_ITEM_COUNT, \
            f"[{TC_ID}] Step 4 FAIL: Item count != {EXPECTED_ITEM_COUNT}"
        assert self.is_cart_icon_visible(), \
            f"[{TC_ID}] Step 4 FAIL: Cart icon not visible"
        logger.info(f"[{TC_ID}] Step 4 ✅ Inventory page fully loaded and validated")
