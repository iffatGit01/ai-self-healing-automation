import allure
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class DashboardPage:
    """Page Object for the Dashboard screen."""

    # ── Locators ──────────────────────────────────────────────
    LOCATORS = {
        "dashboard_section": "#dashboard-section",
        "welcome_message":   "#welcome-msg",
        "balance_display":   "#balance-display",
        "account_number":    "#account-number",
        "logout_button":     "#logout-btn",
    }

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────────

    @allure.step("Click Logout button")
    def logout(self):
        logger.info("Clicking logout button")
        self.page.click(self.LOCATORS["logout_button"])
        self.page.wait_for_selector("#login-section")

    # ── Getters ───────────────────────────────────────────────

    @allure.step("Get welcome message")
    def get_welcome_message(self) -> str:
        self.page.wait_for_selector(self.LOCATORS["welcome_message"])
        return self.page.inner_text(self.LOCATORS["welcome_message"])

    @allure.step("Get current balance")
    def get_balance(self) -> float:
        self.page.wait_for_selector(self.LOCATORS["balance_display"])
        raw = self.page.inner_text(self.LOCATORS["balance_display"])
        return float(raw.replace("$", "").replace(",", ""))

    @allure.step("Get account number")
    def get_account_number(self) -> str:
        return self.page.inner_text(self.LOCATORS["account_number"])

    def is_dashboard_visible(self) -> bool:
        return self.page.is_visible(self.LOCATORS["dashboard_section"])