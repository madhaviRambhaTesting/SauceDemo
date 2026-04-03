# pages/inventory_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("InventoryPage")


class InventoryPage(BasePage):
    """Page Object Model for the SauceDemo Inventory / Dashboard page."""

    # ── Locators ──────────────────────────────────────────────────────────────
    INVENTORY_CONTAINER = (By.CLASS_NAME, "inventory_container")
    APP_LOGO            = (By.CLASS_NAME, "app_logo")
    SHOPPING_CART       = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_SORT        = (By.CLASS_NAME, "product_sort_container")

    # ── Actions ───────────────────────────────────────────────────────────────
    def is_dashboard_displayed(self) -> bool:
        """Verify the dashboard/inventory page is shown after login."""
        logger.info("Verifying inventory/dashboard page is displayed.")
        return (
            self.is_element_visible(*self.INVENTORY_CONTAINER) and
            self.is_element_visible(*self.APP_LOGO)
        )

    def get_app_logo_text(self) -> str:
        return self.get_text(*self.APP_LOGO)

    def is_on_inventory_page(self) -> bool:
        return "inventory.html" in self.get_current_url()
