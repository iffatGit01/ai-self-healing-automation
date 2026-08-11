import allure
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class WithdrawPage:
    """Page Object for the Withdraw section."""

    # ── Locators ──────────────────────────────────────────────
    LOCATORS = {
        "withdraw_amount_input": "#withdraw-amount",
        "withdraw_button":       "#withdraw-btn",
        "withdraw_message":      "#withdraw-msg",
    }

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────────

    @allure.step("Enter withdraw amount: {amount}")
    def enter_amount(self, amount: str):
        logger.info(f"Entering withdraw amount: {amount}")
        self.page.fill(self.LOCATORS["withdraw_amount_input"], str(amount))

    @allure.step("Click Withdraw button")
    def click_withdraw(self):
        logger.info("Clicking withdraw button")
        self.page.click(self.LOCATORS["withdraw_button"])

    @allure.step("Withdraw amount: {amount}")
    def withdraw(self, amount: str):
        self.enter_amount(amount)
        self.click_withdraw()

    # ── Getters ───────────────────────────────────────────────

    @allure.step("Get withdraw message")
    def get_message(self) -> str:
        self.page.wait_for_selector(self.LOCATORS["withdraw_message"])
        return self.page.inner_text(self.LOCATORS["withdraw_message"])

    @allure.step("Get withdraw message class")
    def get_message_class(self) -> str:
        return self.page.get_attribute(
            self.LOCATORS["withdraw_message"], "class"
        )