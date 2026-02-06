"""
Navbar Component for reusable navbar interactions.
"""

from playwright.sync_api import Page, expect


class NavbarComponent:
    """Component object for navbar interactions."""

    def __init__(self, page: Page):
        self.page = page

        # Navbar selectors
        self.navbar = ".navbar"
        self.logout_link = 'a[href="/logout"]'
        self.login_link = 'a[href*="/login"]'
        self.profile_avatar = ".navbar .avatar"
        self.create_post_link = 'a[href="/create-post"]'

    def is_logged_in(self) -> bool:
        """Check if user is logged in by looking for logout link."""
        return self.page.locator(self.logout_link).count() > 0

    def expect_logged_in(self, timeout: int = 5000):
        """Assert that user is logged in (logout link visible)."""
        expect(self.page.locator(self.logout_link)).to_be_visible(timeout=timeout)

    def expect_logged_out(self, timeout: int = 5000):
        """Assert that user is logged out (login link visible)."""
        expect(self.page.locator(self.login_link).first).to_be_visible(timeout=timeout)

    def expect_profile_avatar_visible(self, timeout: int = 5000):
        """Assert that profile avatar is visible (logged in state)."""
        expect(self.page.locator(self.profile_avatar)).to_be_visible(timeout=timeout)

    def expect_create_post_visible(self, timeout: int = 5000):
        """Assert that create post link is visible (logged in state)."""
        expect(self.page.locator(self.create_post_link)).to_be_visible(timeout=timeout)

    def logout(self):
        """Click the logout link."""
        self.page.click(self.logout_link)
        return self
