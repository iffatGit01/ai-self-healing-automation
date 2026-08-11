import pytest
import allure
from automation.pages import WithdrawPage, DepositPage, DashboardPage
from automation.ai import SelfHealer


@allure.feature("Withdrawal")
class TestWithdrawal:

    @allure.story("Valid Withdrawal")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC012_valid_withdrawal(self, authenticated_page):
        healer = SelfHealer(authenticated_page)
        withdraw = WithdrawPage(authenticated_page)
        dashboard = DashboardPage(authenticated_page)

        with allure.step("Get balance before withdrawal"):
            balance_before = dashboard.get_balance()

        with allure.step("Heal withdrawal locators"):
            withdraw.LOCATORS["withdraw_amount_input"] = healer.find_element(
                withdraw.LOCATORS["withdraw_amount_input"], "fill"
            )
            withdraw.LOCATORS["withdraw_button"] = healer.find_element(
                withdraw.LOCATORS["withdraw_button"], "click"
            )

        with allure.step("Withdraw $200"):
            withdraw.withdraw("200")

        with allure.step("Verify success message"):
            message = withdraw.get_message()
            assert "Successfully withdrew" in message, \
                f"Unexpected message: {message}"

        with allure.step("Verify balance decreased by $200"):
            balance_after = dashboard.get_balance()
            assert balance_after == balance_before - 200, \
                f"Expected {balance_before - 200}, got {balance_after}"

    @allure.story("Withdraw Zero")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC013_withdraw_zero(self, authenticated_page):
        withdraw = WithdrawPage(authenticated_page)

        with allure.step("Withdraw $0"):
            withdraw.withdraw("0")

        with allure.step("Verify error message"):
            message = withdraw.get_message()
            assert message == "Please enter a valid amount.", \
                f"Unexpected message: {message}"

    @allure.story("Withdraw Negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC014_withdraw_negative(self, authenticated_page):
        withdraw = WithdrawPage(authenticated_page)

        with allure.step("Withdraw negative amount"):
            withdraw.withdraw("-50")

        with allure.step("Verify error message"):
            message = withdraw.get_message()
            assert message == "Please enter a valid amount.", \
                f"Unexpected message: {message}"

    @allure.story("Insufficient Funds")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC015_insufficient_funds(self, authenticated_page):
        withdraw = WithdrawPage(authenticated_page)

        with allure.step("Withdraw more than balance"):
            withdraw.withdraw("9999")

        with allure.step("Verify insufficient funds message"):
            message = withdraw.get_message()
            assert message == "Insufficient funds.", \
                f"Unexpected message: {message}"

    @allure.story("Withdraw Exceeds Limit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC016_withdraw_exceeds_limit(self, authenticated_page):
        deposit = DepositPage(authenticated_page)
        withdraw = WithdrawPage(authenticated_page)

        with allure.step("Deposit enough funds first"):
            deposit.deposit("15000")

        with allure.step("Withdraw $10,001"):
            withdraw.withdraw("10001")

        with allure.step("Verify limit error message"):
            message = withdraw.get_message()
            assert message == "Maximum withdrawal limit is $10,000.", \
                f"Unexpected message: {message}"

    @allure.story("Withdraw Boundary Value")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC017_withdraw_boundary(self, authenticated_page):
        deposit = DepositPage(authenticated_page)
        withdraw = WithdrawPage(authenticated_page)
        dashboard = DashboardPage(authenticated_page)

        with allure.step("Deposit enough funds first"):
            deposit.deposit("15000")

        with allure.step("Get balance before withdrawal"):
            balance_before = dashboard.get_balance()

        with allure.step("Withdraw exactly $10,000"):
            withdraw.withdraw("10000")

        with allure.step("Verify success message"):
            message = withdraw.get_message()
            assert "Successfully withdrew" in message, \
                f"Unexpected message: {message}"

        with allure.step("Verify balance updated"):
            balance_after = dashboard.get_balance()
            assert balance_after == balance_before - 10000, \
                f"Expected {balance_before - 10000}, got {balance_after}"