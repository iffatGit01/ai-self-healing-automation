import allure
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class TransactionPage:
    """Page Object for the Transaction History section."""

    # ── Locators ──────────────────────────────────────────────
    LOCATORS = {
        "transaction_table":  "#transaction-table",
        "transaction_body":   "#transaction-body",
        "no_transactions":    "#no-transactions",
    }

    def __init__(self, page: Page):
        self.page = page

    # ── Getters ───────────────────────────────────────────────

    @allure.step("Get transaction row by index: {index}")
    def get_transaction_row(self, index: int):
        return self.page.locator(f"#transaction-row-{index}")

    @allure.step("Get all transaction rows")
    def get_all_rows(self):
        return self.page.locator("#transaction-body tr")

    @allure.step("Get transaction count")
    def get_transaction_count(self) -> int:
        rows = self.page.locator(
            "#transaction-body tr:not(#no-transactions)"
        )
        return rows.count()

    @allure.step("Check if no transactions message is visible")
    def is_empty(self) -> bool:
        return self.page.is_visible(self.LOCATORS["no_transactions"])

    @allure.step("Get row data for transaction: {index}")
    def get_row_data(self, index: int) -> dict:
        row = self.page.locator(f"#transaction-row-{index}")
        cells = row.locator("td")
        return {
            "number":        cells.nth(0).inner_text(),
            "type":          cells.nth(1).inner_text(),
            "amount":        cells.nth(2).inner_text(),
            "balance_after": cells.nth(3).inner_text(),
            "datetime":      cells.nth(4).inner_text(),
            "status":        cells.nth(5).inner_text(),
        }