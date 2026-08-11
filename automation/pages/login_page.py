import allure
import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class LoginPage:
    """Page Object for the Login screen."""

    # ── Locators ──────────────────────────────────────────────
    LOCATORS = {
        "username_input":   "#username",
        "password_input":   "#password",
        "login_button":     "#login-btn",
        "login_error":      "#login-error",
        "login_section":    "#login-section",
        "login_card":       "#login-card",
    }

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────────

    @allure.step("Navigate to Login Page")
    def navigate(self, base_url: str):
        logger.info(f"Navigating to {base_url}")
        self.page.goto(base_url)
        self.page.wait_for_selector(self.LOCATORS["login_section"])

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        logger.info(f"Entering username: {username}")
        self.page.fill(self.LOCATORS["username_input"], username)

    @allure.step("Enter password")
    def enter_password(self, password: str):
        logger.info("Entering password")
        self.page.fill(self.LOCATORS["password_input"], password)

    @allure.step("Click Login button")
    def click_login(self):
        logger.info("Clicking login button")
        self.page.click(self.LOCATORS["login_button"])

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertions ────────────────────────────────────────────

    @allure.step("Verify login error message")
    def get_error_message(self) -> str:
        self.page.wait_for_selector(self.LOCATORS["login_error"])
        return self.page.inner_text(self.LOCATORS["login_error"])

    def is_login_page_visible(self) -> bool:
        return self.page.is_visible(self.LOCATORS["login_section"])