import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:5500")
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "100"))


@pytest.fixture(scope="session")
def browser_context():
    """Session-scoped browser context — launched once for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Function-scoped page — fresh page for every test."""
    page = browser_context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page):
    """Page fixture that is already logged in as admin."""
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("#login-btn")
    page.wait_for_selector("#dashboard-section")
    yield page