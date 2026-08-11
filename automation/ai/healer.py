import logging
import os
import allure
from playwright.sync_api import Page
from .ollama_client import OllamaClient
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MAX_RETRIES = int(os.getenv("HEALING_MAX_RETRIES", "3"))
HEALING_ENABLED = os.getenv("HEALING_ENABLED", "true").lower() == "true"
SCREENSHOT_ON_HEAL = os.getenv("HEALING_SCREENSHOT", "true").lower() == "true"


class SelfHealer:
    """
    AI-Powered Self-Healing Engine.

    When a locator fails, this engine:
    1. Captures the current page HTML
    2. Takes a screenshot
    3. Sends both to Ollama/llama3.2
    4. Gets a suggested fix
    5. Retries with the new locator
    6. Logs everything to Allure
    """

    def __init__(self, page: Page):
        self.page = page
        self.client = OllamaClient()
        self.healed_locators: dict = {}  # tracks what was healed

    # ── Core Healing Method ───────────────────────────────────

    def find_element(self, locator: str, action: str = "click"):
        """
        Try to find element with given locator.
        If it fails — trigger AI healing.

        Args:
            locator: CSS/XPath selector string
            action:  What we are trying to do ('click', 'fill', etc.)

        Returns:
            Working locator string (original or healed)
        """
        if not HEALING_ENABLED:
            return locator

        # First — try the original locator
        if self._element_exists(locator):
            logger.info(f"✅ Locator found: {locator}")
            return locator

        # Locator failed — start healing
        logger.warning(f"⚠️ Locator broken: {locator} — Starting AI healing...")
        return self._heal(locator, action)

    # ── Healing Logic ─────────────────────────────────────────

    def _heal(self, broken_locator: str, action: str) -> str:
        """Run the AI healing loop."""

        # Take screenshot of broken state
        screenshot_path = self._take_screenshot(broken_locator)

        # Get current page HTML
        html = self._get_page_html()

        healed_locator = None

        for attempt in range(1, MAX_RETRIES + 1):
            logger.info(f"🔄 Healing attempt {attempt}/{MAX_RETRIES}")

            try:
                # Build prompt for Ollama
                prompt = self._build_prompt(
                    broken_locator, html, action, attempt
                )

                # Ask Ollama for fix
                suggestion = self.client.ask(prompt)
                suggestion = self._clean_suggestion(suggestion)

                logger.info(
                    f"🤖 AI suggested locator (attempt {attempt}): {suggestion}"
                )

                # Test the suggested locator
                if self._element_exists(suggestion):
                    healed_locator = suggestion
                    logger.info(f"✅ Healed! New locator: {healed_locator}")

                    # Log to Allure
                    self._log_healing_to_allure(
                        broken_locator,
                        healed_locator,
                        attempt,
                        screenshot_path
                    )

                    # Store healed locator for reporting
                    self.healed_locators[broken_locator] = healed_locator
                    break
                else:
                    logger.warning(
                        f"❌ Suggested locator not found: {suggestion}"
                    )

            except Exception as e:
                logger.error(f"Healing attempt {attempt} failed: {e}")

        if not healed_locator:
            logger.error(
                f"💀 All {MAX_RETRIES} healing attempts failed "
                f"for locator: {broken_locator}"
            )
            self._log_failure_to_allure(broken_locator, screenshot_path)
            raise Exception(
                f"Self-healing failed after {MAX_RETRIES} attempts "
                f"for locator: {broken_locator}"
            )

        return healed_locator

    # ── Prompt Builder ────────────────────────────────────────

    def _build_prompt(
        self,
        broken_locator: str,
        html: str,
        action: str,
        attempt: int
    ) -> str:
        """Build a clear prompt for the LLM."""

        # Trim HTML to avoid token limits
        html_snippet = html[:4000] if len(html) > 4000 else html

        return f"""
A Playwright automation test is failing because this locator no longer works:

BROKEN LOCATOR: {broken_locator}
INTENDED ACTION: {action}
ATTEMPT: {attempt} of {MAX_RETRIES}

Here is the current HTML of the page:
---
{html_snippet}
---

Task:
- Find the correct element in the HTML that matches the intended action
- Suggest a new valid CSS selector or XPath that will work with Playwright
- Return ONLY the locator string, nothing else
- Example format: #element-id  OR  .class-name  OR  //button[@type='submit']

Your suggested locator:
"""

    # ── Helpers ───────────────────────────────────────────────

    def _element_exists(self, locator: str) -> bool:
        """Check if element exists on the page."""
        try:
            element = self.page.locator(locator)
            return element.count() > 0
        except Exception:
            return False

    def _get_page_html(self) -> str:
        """Get current page HTML content."""
        try:
            return self.page.content()
        except Exception as e:
            logger.error(f"Failed to get page HTML: {e}")
            return ""

    def _take_screenshot(self, locator: str) -> str:
        """Take screenshot when locator fails."""
        if not SCREENSHOT_ON_HEAL:
            return ""
        try:
            safe_name = locator.replace(
                "#", "").replace(".", "").replace("/", "_")
            path = f"allure-results/healing_{safe_name}.png"
            os.makedirs("allure-results", exist_ok=True)
            self.page.screenshot(path=path)
            logger.info(f"📸 Screenshot saved: {path}")
            return path
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return ""

    def _clean_suggestion(self, suggestion: str) -> str:
        """Clean up the LLM response to extract just the locator."""
        suggestion = suggestion.strip()
        # Remove markdown code blocks if present
        suggestion = suggestion.replace("```", "").strip()
        # Take only first line if multiple lines returned
        suggestion = suggestion.split("\n")[0].strip()
        return suggestion

    # ── Allure Logging ────────────────────────────────────────

    def _log_healing_to_allure(
        self,
        broken: str,
        healed: str,
        attempt: int,
        screenshot_path: str
    ):
        """Attach healing details to Allure report."""
        allure.attach(
            body=(
                f"🔴 Broken Locator : {broken}\n"
                f"✅ Healed Locator : {healed}\n"
                f"🔄 Healed on Attempt: {attempt}"
            ),
            name="Self-Healing Report",
            attachment_type=allure.attachment_type.TEXT
        )
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    body=f.read(),
                    name="Screenshot at Failure",
                    attachment_type=allure.attachment_type.PNG
                )

    def _log_failure_to_allure(self, broken: str, screenshot_path: str):
        """Attach failure details to Allure report."""
        allure.attach(
            body=(
                f"💀 Failed to heal locator: {broken}\n"
                f"Attempts made: {MAX_RETRIES}"
            ),
            name="Self-Healing FAILED",
            attachment_type=allure.attachment_type.TEXT
        )
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    body=f.read(),
                    name="Screenshot at Final Failure",
                    attachment_type=allure.attachment_type.PNG
                )