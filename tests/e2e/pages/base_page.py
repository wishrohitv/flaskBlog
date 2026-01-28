"""
Base Page Object with common methods for all pages.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common functionality."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Common selectors
        self.flash_toast = ".toast"
        self.flash_alert = ".alert"
        self.flash_success = ".alert-success"
        self.flash_error = ".alert-error"

    def navigate(self, path: str = "/"):
        """Navigate to a path relative to base URL."""
        url = f"{self.base_url}{path}"
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    def get_flash_message(self) -> str | None:
        """Get the text content of the flash message if present."""
        alert = self.page.locator(self.flash_alert).first
        if alert.count() > 0:
            return alert.text_content()
        return None

    def get_flash_messages(self) -> list[str]:
        """Get all flash message texts."""
        alerts = self.page.locator(self.flash_alert)
        messages = []
        for i in range(alerts.count()):
            text = alerts.nth(i).text_content()
            if text:
                messages.append(text.strip())
        return messages

    def expect_success_flash(self, timeout: int = 5000):
        """Assert that a success flash message is displayed."""
        expect(self.page.locator(self.flash_success).first).to_be_visible(
            timeout=timeout
        )

    def expect_error_flash(self, timeout: int = 5000):
        """Assert that an error flash message is displayed."""
        expect(self.page.locator(self.flash_error).first).to_be_visible(timeout=timeout)

    def expect_flash_contains(self, text: str, timeout: int = 5000):
        """Assert that a flash message contains specific text."""
        expect(self.page.locator(self.flash_alert).first).to_contain_text(
            text, timeout=timeout
        )

    def wait_for_navigation(self, url_pattern: str = None, timeout: int = 5000):
        """Wait for page navigation to complete."""
        if url_pattern:
            self.page.wait_for_url(url_pattern, timeout=timeout)
        else:
            self.page.wait_for_load_state("networkidle", timeout=timeout)

    def is_logged_in(self) -> bool:
        """Check if user is logged in by looking for logout link in navbar."""
        logout_link = self.page.locator('a[href="/logout"]')
        return logout_link.count() > 0

    def get_page_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def take_screenshot(self, name: str):
        """Take a screenshot for debugging."""
        self.page.screenshot(path=f"screenshots/{name}.png")
