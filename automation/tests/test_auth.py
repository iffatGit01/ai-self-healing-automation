import pytest
import allure
from automation.pages import LoginPage, DashboardPage
from automation.ai import SelfHealer


@allure.feature("Authentication")
class TestAuthentication:

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC001_valid_login(self, page):
        healer = SelfHealer(page)
        login = LoginPage(page)
        dashboard = DashboardPage(page)

        with allure.step("Heal and verify login locators"):
            login.LOCATORS["username_input"] = healer.find_element(
                login.LOCATORS["username_input"], "fill"
            )
            login.LOCATORS["password_input"] = healer.find_element(
                login.LOCATORS["password_input"], "fill"
            )
            login.LOCATORS["login_button"] = healer.find_element(
                login.LOCATORS["login_button"], "click"
            )

        with allure.step("Perform login with valid credentials"):
            login.login("admin", "admin123")

        with allure.step("Verify dashboard is visible"):
            assert dashboard.is_dashboard_visible(), \
                "Dashboard should be visible after login"

        with allure.step("Verify welcome message"):
            welcome = dashboard.get_welcome_message()
            assert "admin" in welcome, \
                f"Expected 'admin' in welcome message, got: {welcome}"

    @allure.story("Invalid Password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC002_invalid_password(self, page):
        healer = SelfHealer(page)
        login = LoginPage(page)

        with allure.step("Heal login locators"):
            login.LOCATORS["username_input"] = healer.find_element(
                login.LOCATORS["username_input"], "fill"
            )
            login.LOCATORS["password_input"] = healer.find_element(
                login.LOCATORS["password_input"], "fill"
            )
            login.LOCATORS["login_button"] = healer.find_element(
                login.LOCATORS["login_button"], "click"
            )

        with allure.step("Login with wrong password"):
            login.login("admin", "wrongpass")

        with allure.step("Verify error message"):
            error = login.get_error_message()
            assert error == "Invalid username or password.", \
                f"Unexpected error message: {error}"

    @allure.story("Invalid Username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC003_invalid_username(self, page):
        login = LoginPage(page)

        with allure.step("Login with invalid username"):
            login.login("ghost", "admin123")

        with allure.step("Verify error message"):
            error = login.get_error_message()
            assert error == "Invalid username or password.", \
                f"Unexpected error message: {error}"

    @allure.story("Empty Fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC004_empty_fields(self, page):
        login = LoginPage(page)

        with allure.step("Click login without entering credentials"):
            login.click_login()

        with allure.step("Verify error message"):
            error = login.get_error_message()
            assert error == "Please enter username and password.", \
                f"Unexpected error message: {error}"

    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_TC005_logout(self, authenticated_page):
        healer = SelfHealer(authenticated_page)
        dashboard = DashboardPage(authenticated_page)
        login = LoginPage(authenticated_page)

        with allure.step("Verify dashboard is visible"):
            assert dashboard.is_dashboard_visible(), \
                "Dashboard should be visible before logout"

        with allure.step("Heal logout button locator"):
            dashboard.LOCATORS["logout_button"] = healer.find_element(
                dashboard.LOCATORS["logout_button"], "click"
            )

        with allure.step("Click logout"):
            dashboard.logout()

        with allure.step("Verify login page is visible"):
            assert login.is_login_page_visible(), \
                "Login page should be visible after logout"