import pytest
import allure
from automation.pages import (
    TransactionPage, DepositPage,
    WithdrawPage, DashboardPage
)
from automation.ai import SelfHealer


@allure.feature("Transaction History")
class TestTransactions:

    @allure.story("No Transactions on Fresh Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC018_no_transactions(self, authenticated_page):
        healer = SelfHealer(authenticated_page)
        transaction = TransactionPage(authenticated_page)

        with allure.step("Heal transaction table locator"):
            transaction.LOCATORS["no_transactions"] = healer.find_element(
                transaction.LOCATORS["no_transactions"], "visible"
            )

        with allure.step("Verify no transactions message"):
            assert transaction.is_empty(), \
                "Transaction table should be empty on fresh login"

    @allure.story("Deposit Adds Transaction Row")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC019_deposit_adds_row(self, authenticated_page):
        deposit = DepositPage(authenticated_page)
        transaction = TransactionPage(authenticated_page)

        with allure.step("Make a deposit"):
            deposit.deposit("100")

        with allure.step("Verify transaction row added"):
            row = transaction.get_row_data(1)
            assert row["type"] == "Deposit", \
                f"Expected 'Deposit', got: {row['type']}"
            assert row["amount"] == "$100.00", \
                f"Expected '$100.00', got: {row['amount']}"
            assert row["status"] == "Success", \
                f"Expected 'Success', got: {row['status']}"

    @allure.story("Failed Transaction Adds Row")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC020_failed_transaction_adds_row(self, authenticated_page):
        withdraw = WithdrawPage(authenticated_page)
        transaction = TransactionPage(authenticated_page)

        with allure.step("Attempt withdrawal exceeding balance"):
            withdraw.withdraw("9999")

        with allure.step("Verify failed transaction row added"):
            row = transaction.get_row_data(1)
            assert row["type"] == "Withdrawal", \
                f"Expected 'Withdrawal', got: {row['type']}"
            assert row["status"] == "Failed", \
                f"Expected 'Failed', got: {row['status']}"

    @allure.story("Multiple Transactions in Reverse Order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC021_multiple_transactions_order(self, authenticated_page):
        deposit = DepositPage(authenticated_page)
        withdraw = WithdrawPage(authenticated_page)
        transaction = TransactionPage(authenticated_page)

        with allure.step("Make a deposit"):
            deposit.deposit("300")

        with allure.step("Make a withdrawal"):
            withdraw.withdraw("100")

        with allure.step("Verify 2 transactions exist"):
            count = transaction.get_transaction_count()
            assert count == 2, f"Expected 2 transactions, got: {count}"

        with allure.step("Verify latest transaction appears first"):
            all_rows = transaction.get_all_rows()
            first_row_id = all_rows.nth(0).get_attribute("id")
            assert first_row_id == "transaction-row-2", \
                f"Expected row-2 first, got: {first_row_id}"