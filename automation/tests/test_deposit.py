import pytest
import allure
from automation.pages import DepositPage, DashboardPage
from automation.ai import SelfHealer


@allure.feature("Deposit")
class TestDeposit:

    @allure.story("Valid Deposit")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC006_valid_deposit(self, authenticated_page):
        healer = SelfHealer(authenticated_page)
        deposit = DepositPage(authenticated_page)
        dashboard = DashboardPage(authenticated_page)

        with allure.step("Get balance before deposit"):
            balance_before = dashboard.get_balance()

        with allure.step("Heal deposit locators"):
            deposit.LOCATORS["deposit_amount_input"] = healer.find_element(
                deposit.LOCATORS["deposit_amount_input"], "fill"
            )
            deposit.LOCATORS["deposit_button"] = healer.find_element(
                deposit.LOCATORS["deposit_button"], "click"
            )

        with allure.step("Deposit $500"):
            deposit.deposit("500")

        with allure.step("Verify success message"):
            message = deposit.get_message()
            assert "Successfully deposited" in message, \
                f"Unexpected message: {message}"

        with allure.step("Verify balance increased by $500"):
            balance_after = dashboard.get_balance()
            assert balance_after == balance_before + 500, \
                f"Expected {balance_before + 500}, got {balance_after}"

    @allure.story("Deposit Zero")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC007_deposit_zero(self, authenticated_page):
        deposit = DepositPage(authenticated_page)

        with allure.step("Deposit $0"):
            deposit.deposit("0")

        with allure.step("Verify error message"):
            message = deposit.get_message()
            assert message == "Please enter a valid amount.", \
                f"Unexpected message: {message}"

        with allure.step("Verify message is error type"):
            css_class = deposit.get_message_class()
            assert "error" in css_class, \
                f"Expected error class, got: {css_class}"

    @allure.story("Deposit Negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC008_deposit_negative(self, authenticated_page):
        deposit = DepositPage(authenticated_page)

        with allure.step("Deposit negative amount"):
            deposit.deposit("-100")

        with allure.step("Verify error message"):
            message = deposit.get_message()
            assert message == "Please enter a valid amount.", \
                f"Unexpected message: {message}"

    @allure.story("Deposit Exceeds Limit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC009_deposit_exceeds_limit(self, authenticated_page):
        deposit = DepositPage(authenticated_page)

        with allure.step("Deposit $100,001"):
            deposit.deposit("100001")

        with allure.step("Verify limit error message"):
            message = deposit.get_message()
            assert message == "Maximum deposit limit is $100,000.", \
                f"Unexpected message: {message}"

    @allure.story("Deposit Boundary Value")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC011_deposit_boundary(self, authenticated_page):
        deposit = DepositPage(authenticated_page)
        dashboard = DashboardPage(authenticated_page)

        with allure.step("Get balance before deposit"):
            balance_before = dashboard.get_balance()

        with allure.step("Deposit exactly $100,000"):
            deposit.deposit("100000")

        with allure.step("Verify success message"):
            message = deposit.get_message()
            assert "Successfully deposited" in message, \
                f"Unexpected message: {message}"

        with allure.step("Verify balance updated"):
            balance_after = dashboard.get_balance()
            assert balance_after == balance_before + 100000, \
                f"Expected {balance_before + 100000}, got {balance_after}"