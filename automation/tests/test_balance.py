import pytest
import allure
from automation.pages import DashboardPage, DepositPage, WithdrawPage
from automation.ai import SelfHealer


@allure.feature("Balance Display")
class TestBalance:

    @allure.story("Balance on Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC023_balance_on_login(self, page):
        from automation.pages import LoginPage
        healer = SelfHealer(page)
        login = LoginPage(page)
        dashboard = DashboardPage(page)

        with allure.step("Login as john"):
            login.login("john", "john456")

        with allure.step("Heal balance locator"):
            dashboard.LOCATORS["balance_display"] = healer.find_element(
                dashboard.LOCATORS["balance_display"], "read"
            )

        with allure.step("Verify starting balance is $500.00"):
            balance = dashboard.get_balance()
            assert balance == 500.00, \
                f"Expected 500.00, got: {balance}"

    @allure.story("Balance After Deposit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC024_balance_after_deposit(self, page):
        from automation.pages import LoginPage
        login = LoginPage(page)
        dashboard = DashboardPage(page)
        deposit = DepositPage(page)

        with allure.step("Login as john"):
            login.login("john", "john456")

        with allure.step("Deposit $250"):
            deposit.deposit("250")

        with allure.step("Verify balance is $750.00"):
            balance = dashboard.get_balance()
            assert balance == 750.00, \
                f"Expected 750.00, got: {balance}"

    @allure.story("Balance After Withdrawal")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC025_balance_after_withdrawal(self, page):
        from automation.pages import LoginPage
        login = LoginPage(page)
        dashboard = DashboardPage(page)
        withdraw = WithdrawPage(page)

        with allure.step("Login as john"):
            login.login("john", "john456")

        with allure.step("Withdraw $100"):
            withdraw.withdraw("100")

        with allure.step("Verify balance is $400.00"):
            balance = dashboard.get_balance()
            assert balance == 400.00, \
                f"Expected 400.00, got: {balance}"