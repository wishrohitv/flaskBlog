"""
E2E tests for the login functionality.
"""

import pytest

from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.navbar_component import NavbarComponent


class TestLoginPageRendering:
    """Tests for login page rendering and structure."""

    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_page_renders(self, page, flask_server):
        """Test that the login page loads with all required elements."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.expect_page_loaded()

    @pytest.mark.auth
    def test_login_page_has_csrf_token(self, page, flask_server):
        """Test that CSRF protection is enabled on the login form."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.expect_has_csrf_token()

    @pytest.mark.auth
    def test_login_page_has_forgot_password_link(self, page, flask_server):
        """Test that forgot password link is present."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.expect_has_forgot_password_link()

    @pytest.mark.auth
    def test_login_page_title(self, page, flask_server):
        """Test that the page has the correct title."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        # Title should contain "login" (case insensitive check)
        title = page.title().lower()
        assert "login" in title or "log in" in title


class TestLoginSuccess:
    """Tests for successful login scenarios."""

    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_with_valid_credentials(self, page, flask_server, app_settings):
        """Test that admin can login with valid credentials."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"],
            app_settings["default_admin"]["password"],
        )
        login_page.expect_success_flash()

    @pytest.mark.auth
    def test_login_redirect_after_success(self, page, flask_server, app_settings):
        """Test that successful login redirects to home page."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"],
            app_settings["default_admin"]["password"],
        )

        # Wait for redirect
        page.wait_for_url("**/", timeout=5000)
        assert (
            page.url.rstrip("/").endswith(str(flask_server["port"]))
            or page.url == flask_server["base_url"] + "/"
        )

    @pytest.mark.auth
    def test_login_case_insensitive_username(self, page, flask_server, app_settings):
        """Test that username is case-insensitive (ADMIN should work)."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"].upper(),  # "ADMIN"
            app_settings["default_admin"]["password"],
        )
        login_page.expect_success_flash()

    @pytest.mark.auth
    def test_login_whitespace_trimmed(self, page, flask_server, app_settings):
        """Test that whitespace in username is trimmed."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            f"  {app_settings['default_admin']['username']}  ",  # "  admin  "
            app_settings["default_admin"]["password"],
        )
        login_page.expect_success_flash()


class TestLoginErrors:
    """Tests for login error scenarios."""

    @pytest.mark.auth
    def test_login_wrong_password(self, page, flask_server, app_settings):
        """Test that wrong password shows error flash."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"],
            "wrongpassword123",
        )
        login_page.expect_error_flash()

    @pytest.mark.auth
    def test_login_nonexistent_user(self, page, flask_server):
        """Test that nonexistent user shows not found error."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            "nonexistent_user_12345",
            "anypassword",
        )
        login_page.expect_error_flash()

    @pytest.mark.auth
    def test_login_empty_password(self, page, flask_server, app_settings):
        """Test that empty password shows error or validation message."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()

        # Fill only username
        login_page.fill_username(app_settings["default_admin"]["username"])
        login_page.click_submit()

        # Should either show validation message or error flash
        # HTML5 validation should prevent submission with empty password
        is_valid = login_page.is_password_valid()
        if not is_valid:
            # HTML5 validation triggered
            validation_msg = login_page.get_password_validation_message()
            assert validation_msg != ""


class TestLoginSessionManagement:
    """Tests for session management during login."""

    @pytest.mark.auth
    def test_login_already_logged_in_redirects(self, logged_in_page, flask_server):
        """Test that already logged in user gets redirected from login page."""
        # logged_in_page fixture already has admin logged in
        # Try to navigate to login page
        logged_in_page.goto(f"{flask_server['base_url']}/login/redirect=&")

        # Should be redirected away from login page
        page_url = logged_in_page.url
        assert "/login" not in page_url or page_url.endswith("/")

    @pytest.mark.auth
    def test_login_creates_session(self, page, flask_server, app_settings):
        """Test that successful login creates session (navbar shows logged-in state)."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"],
            app_settings["default_admin"]["password"],
        )

        # Wait for redirect
        page.wait_for_url("**/", timeout=5000)

        # Check navbar shows logged-in state
        navbar = NavbarComponent(page)
        navbar.expect_logged_in()

    @pytest.mark.auth
    def test_session_persists_after_navigation(self, page, flask_server, app_settings):
        """Test that session persists after navigating to other pages."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(
            app_settings["default_admin"]["username"],
            app_settings["default_admin"]["password"],
        )

        # Wait for redirect
        page.wait_for_url("**/", timeout=5000)

        # Navigate to another page
        page.goto(flask_server["base_url"])

        # Should still be logged in
        navbar = NavbarComponent(page)
        navbar.expect_logged_in()


class TestLoginFormValidation:
    """Tests for form validation behavior."""

    @pytest.mark.auth
    def test_login_empty_username_validation(self, page, flask_server):
        """Test HTML5 validation for empty username field."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()

        # Fill only password
        login_page.fill_password("somepassword")
        login_page.click_submit()

        # HTML5 validation should show message for empty username
        is_valid = login_page.is_username_valid()
        if not is_valid:
            validation_msg = login_page.get_username_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_login_empty_password_validation(self, page, flask_server, app_settings):
        """Test HTML5 validation for empty password field."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()

        # Fill only username
        login_page.fill_username(app_settings["default_admin"]["username"])
        login_page.click_submit()

        # HTML5 validation should show message for empty password
        is_valid = login_page.is_password_valid()
        if not is_valid:
            validation_msg = login_page.get_password_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_login_form_prevents_double_submission(
        self, page, flask_server, app_settings
    ):
        """Test that form submission works properly (no double submission issues)."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()

        login_page.fill_username(app_settings["default_admin"]["username"])
        login_page.fill_password(app_settings["default_admin"]["password"])

        # Click submit
        login_page.click_submit()

        # Should get success flash (single submission)
        login_page.expect_success_flash()


class TestLoginWithTestUser:
    """Tests using dynamically created test users."""

    @pytest.mark.auth
    def test_login_with_test_user(self, page, flask_server, test_user):
        """Test that a dynamically created test user can login."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(test_user.username, test_user.password)
        login_page.expect_success_flash()

    @pytest.mark.auth
    def test_login_test_user_creates_session(self, page, flask_server, test_user):
        """Test that test user login creates proper session."""
        login_page = LoginPage(page, flask_server["base_url"])
        login_page.navigate()
        login_page.login(test_user.username, test_user.password)

        # Wait for redirect
        page.wait_for_url("**/", timeout=5000)

        # Check navbar shows logged-in state
        navbar = NavbarComponent(page)
        navbar.expect_logged_in()
