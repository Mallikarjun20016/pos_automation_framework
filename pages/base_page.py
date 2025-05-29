from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url):
        self.page.goto(url)
        logger.info(f"Navigated to {url}")

    def click_element(self, selector):
        self.page.wait_for_selector(selector).click()
        logger.info(f"Clicked element: {selector}")

    def fill_text(self, selector, text):
        self.page.wait_for_selector(selector).fill(text)
        logger.info(f"Filled {selector} with value: {text}")

    def press_enter(self, selector):
        """Press the Enter key on an element identified by the given selector."""
        self.page.wait_for_selector(selector, state="visible")
        self.page.press(selector, "Enter")
        logger.info(f"Pressed Enter on element: {selector}")

    def wait_for_element(self, selector, timeout=5000):
        """Waits for an element to be visible on the page."""
        self.page.wait_for_selector(selector, timeout=timeout)
        logger.info(f"Waited for element: {selector}")

    def paste_text(self, selector, text):
        """Pastes the given text into the input field, clearing existing content."""
        self.page.wait_for_selector(selector)
        self.page.locator(selector).fill('')  # Clear the input field first
        self.page.locator(selector).type(text)  # Type the text dynamically
        logger.info(f"Pasted value into {selector}: {text}")

    def get_text(self, selector):
        """Returns the text content of the given element."""
        self.page.wait_for_selector(selector)
        text = self.page.locator(selector).inner_text()
        logger.info(f"Got text from {selector}: {text}")
        return text

    def get_value(self, selector):
        self.page.wait_for_selector(selector)
        return self.page.input_value(selector)

    def verify_text(self, selector, expected_text):
        text = self.page.wait_for_selector(selector).inner_text()
        assert text.strip() == expected_text, f"Expected {expected_text}, but got {text}"
        logger.info(f"Verified text: {expected_text} at {selector}")

    def is_element_visible(self, selector: str, timeout: int = 5) -> bool:
        """Check if an element is visible within the given timeout."""
        try:
            self.page.wait_for_selector(selector, timeout=timeout * 1000, state="visible")
            return True
        except Exception:
            return False

    def get_element_attribute(self, selector: str, attribute: str) -> str:
        try:
            value = self.page.locator(selector).get_attribute(attribute)
            logger.info(f"Extracted attribute '{attribute}' with value '{value}' from element: {selector}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute '{attribute}' from {selector}: {str(e)}")
            raise