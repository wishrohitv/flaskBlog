"""
Signup Page Object for interacting with the signup form.
"""

from playwright.sync_api import Page, expect

from tests.e2e.pages.base_page import BasePage


class SignupPage(BasePage):
    """Page object for the signup page."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # Signup form selectors
        self.username_input = 'input[name="username"]'
        self.email_input = 'input[name="email"]'
        self.password_input = 'input[name="password"]'
        self.password_confirm_input = 'input[name="password_confirm"]'
        self.submit_button = 'button[type="submit"]'
        self.csrf_token = 'input[name="csrf_token"]'
        self.privacy_policy_link = 'a[href="/privacy-policy"]'

    def navigate(self, path: str = "/signup"):
        """Navigate to the signup page."""
        return super().navigate(path)

    def fill_username(self, username: str):
        """Fill in the username field."""
        self.page.fill(self.username_input, username)
        return self

    def fill_email(self, email: str):
        """Fill in the email field."""
        self.page.fill(self.email_input, email)
        return self

    def fill_password(self, password: str):
        """Fill in the password field."""
        self.page.fill(self.password_input, password)
        return self

    def fill_password_confirm(self, password_confirm: str):
        """Fill in the password confirmation field."""
        self.page.fill(self.password_confirm_input, password_confirm)
        return self

    def click_submit(self):
        """Click the submit/signup button."""
        self.page.click(self.submit_button)
        return self

    def signup(
        self, username: str, email: str, password: str, password_confirm: str = None
    ):
        """
        Perform signup with given credentials.
        If password_confirm is not provided, uses the same value as password.
        Does not wait for navigation - caller should handle that.
        """
        if password_confirm is None:
            password_confirm = password

        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)
        self.fill_password_confirm(password_confirm)
        self.click_submit()
        return self

    def signup_and_expect_error(
        self,
        username: str,
        email: str,
        password: str,
        password_confirm: str = None,
        timeout: int = 5000,
    ):
        """Signup and verify failed signup with error flash message."""
        self.signup(username, email, password, password_confirm)
        self.expect_error_flash(timeout=timeout)
        return self

    def expect_page_loaded(self):
        """Verify that all signup page elements are present."""
        expect(self.page.locator(self.username_input)).to_be_visible()
        expect(self.page.locator(self.email_input)).to_be_visible()
        expect(self.page.locator(self.password_input)).to_be_visible()
        expect(self.page.locator(self.password_confirm_input)).to_be_visible()
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

    def expect_has_privacy_policy_link(self):
        """Verify privacy policy link is present."""
        expect(self.page.locator(self.privacy_policy_link)).to_be_visible()
        return self

    def get_username_validation_message(self) -> str:
        """Get HTML5 validation message for username field."""
        return self.page.locator(self.username_input).evaluate(
            "el => el.validationMessage"
        )

    def get_email_validation_message(self) -> str:
        """Get HTML5 validation message for email field."""
        return self.page.locator(self.email_input).evaluate(
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

    def is_email_valid(self) -> bool:
        """Check if email field passes HTML5 validation."""
        return self.page.locator(self.email_input).evaluate("el => el.validity.valid")

    def is_password_valid(self) -> bool:
        """Check if password field passes HTML5 validation."""
        return self.page.locator(self.password_input).evaluate(
            "el => el.validity.valid"
        )

    def get_username_max_length(self) -> int:
        """Get the maxlength attribute of the username field."""
        return int(
            self.page.locator(self.username_input).get_attribute("maxlength") or 0
        )
