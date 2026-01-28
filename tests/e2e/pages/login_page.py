"""
Login Page Object for interacting with the login form.
"""

from playwright.sync_api import Page, expect

from tests.e2e.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # Login form selectors
        self.username_input = 'input[name="username"]'
        self.password_input = 'input[name="password"]'
        self.submit_button = 'button[type="submit"]'
        self.csrf_token = 'input[name="csrf_token"]'
        self.forgot_password_link = 'a[href*="password_reset"]'
        self.login_card = ".card"
        self.card_title = ".card-title"

    def navigate(self, path: str = "/login/redirect=&"):
        """Navigate to the login page."""
        return super().navigate(path)

    def fill_username(self, username: str):
        """Fill in the username field."""
        self.page.fill(self.username_input, username)
        return self

    def fill_password(self, password: str):
        """Fill in the password field."""
        self.page.fill(self.password_input, password)
        return self

    def click_submit(self):
        """Click the submit/login button."""
        self.page.click(self.submit_button)
        return self

    def login(self, username: str, password: str):
        """
        Perform login with given credentials.
        Does not wait for navigation - caller should handle that.
        """
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit()
        return self

    def login_and_expect_success(
        self, username: str, password: str, timeout: int = 5000
    ):
        """Login and verify successful login with flash message."""
        self.login(username, password)
        self.expect_success_flash(timeout=timeout)
        return self

    def login_and_expect_error(self, username: str, password: str, timeout: int = 5000):
        """Login and verify failed login with error flash message."""
        self.login(username, password)
        self.expect_error_flash(timeout=timeout)
        return self

    def expect_page_loaded(self):
        """Verify that all login page elements are present."""
        expect(self.page.locator(self.username_input)).to_be_visible()
        expect(self.page.locator(self.password_input)).to_be_visible()
        expect(self.page.locator(self.submit_button)).to_be_visible()
        expect(self.page.locator(self.csrf_token)).to_be_attached()
        return self

    def expect_has_csrf_token(self):
        """Verify CSRF token is present in the form."""
        csrf = self.page.locator(self.csrf_token)
        expect(csrf).to_be_attached()
        value = csrf.get_attribute("value")
        assert value and len(value) > 0, "CSRF token should have a value"
        return self

    def expect_has_forgot_password_link(self):
        """Verify forgot password link is present."""
        expect(self.page.locator(self.forgot_password_link)).to_be_visible()
        return self

    def click_forgot_password(self):
        """Click the forgot password link."""
        self.page.click(self.forgot_password_link)
        return self

    def get_username_validation_message(self) -> str:
        """Get HTML5 validation message for username field."""
        return self.page.locator(self.username_input).evaluate(
            "el => el.validationMessage"
        )

    def get_password_validation_message(self) -> str:
        """Get HTML5 validation message for password field."""
        return self.page.locator(self.password_input).evaluate(
            "el => el.validationMessage"
        )

    def is_username_valid(self) -> bool:
        """Check if username field passes HTML5 validation."""
        return self.page.locator(self.username_input).evaluate(
            "el => el.validity.valid"
        )

    def is_password_valid(self) -> bool:
        """Check if password field passes HTML5 validation."""
        return self.page.locator(self.password_input).evaluate(
            "el => el.validity.valid"
        )
