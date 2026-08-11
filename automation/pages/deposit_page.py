import allure
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class DepositPage:
    """Page Object for the Deposit section."""

    # ── Locators ──────────────────────────────────────────────
    LOCATORS = {
        "deposit_amount_input": "#deposit-amount",
        "deposit_button":       "#deposit-btn",
        "deposit_message":      "#deposit-msg",
    }

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────────

    @allure.step("Enter deposit amount: {amount}")
    def enter_amount(self, amount: str):
        logger.info(f"Entering deposit amount: {amount}")
        self.page.fill(self.LOCATORS["deposit_amount_input"], str(amount))

    @allure.step("Click Deposit button")
    def click_deposit(self):
        logger.info("Clicking deposit button")
        self.page.click(self.LOCATORS["deposit_button"])

    @allure.step("Deposit amount: {amount}")
    def deposit(self, amount: str):
        self.enter_amount(amount)
        self.click_deposit()

    # ── Getters ───────────────────────────────────────────────

    @allure.step("Get deposit message")
    def get_message(self) -> str:
        self.page.wait_for_selector(self.LOCATORS["deposit_message"])
        return self.page.inner_text(self.LOCATORS["deposit_message"])

    @allure.step("Get deposit message class")
    def get_message_class(self) -> str:
        return self.page.get_attribute(
            self.LOCATORS["deposit_message"], "class"
        )