import logging
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for communicating with local Ollama LLM."""

    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        logger.info(f"OllamaClient initialized with model: {self.model}")

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and return the response text.
        """
        try:
            logger.info(f"Sending prompt to Ollama model: {self.model}")
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert QA automation engineer "
                            "specializing in Playwright and web locators. "
                            "You analyze broken locators and suggest fixes "
                            "based on the page HTML. "
                            "Always respond with ONLY the fixed locator string, "
                            "nothing else. No explanation, no markdown, "
                            "just the raw locator."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            result = response["message"]["content"].strip()
            logger.info(f"Ollama response: {result}")
            return result

        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise

    def is_available(self) -> bool:
        """Check if Ollama service is running."""
        try:
            ollama.list()
            return True
        except Exception:
            return False