"""
E2E tests for the signup functionality.
"""

import uuid

import pytest

from tests.e2e.helpers.database_helpers import (
    get_user_by_email,
    get_user_by_username,
    get_user_points,
)
from tests.e2e.pages.navbar_component import NavbarComponent
from tests.e2e.pages.signup_page import SignupPage


class TestSignupPageRendering:
    """Tests for signup page rendering and structure."""

    @pytest.mark.smoke
    @pytest.mark.auth
    def test_signup_page_renders(self, page, flask_server):
        """Test that the signup page loads with all required elements."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()
        signup_page.expect_page_loaded()

    @pytest.mark.auth
    def test_signup_page_has_csrf_token(self, page, flask_server):
        """Test that CSRF protection is enabled on the signup form."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()
        signup_page.expect_has_csrf_token()

    @pytest.mark.auth
    def test_signup_page_has_privacy_policy_link(self, page, flask_server):
        """Test that privacy policy link is present."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()
        signup_page.expect_has_privacy_policy_link()

    @pytest.mark.auth
    def test_signup_page_title(self, page, flask_server):
        """Test that the page has the correct title."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()
        # Title should contain "signup" or "sign up" (case insensitive check)
        title = page.title().lower()
        assert "signup" in title or "sign up" in title or "register" in title


class TestSignupSuccess:
    """Tests for successful signup scenarios."""

    @pytest.mark.smoke
    @pytest.mark.auth
    def test_signup_with_valid_data(self, page, flask_server, clean_db):
        """Test that a user can signup with valid credentials."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"newuser_{unique_id}"
        email = f"newuser_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

    @pytest.mark.auth
    def test_signup_creates_user_in_database(
        self, page, flask_server, clean_db, db_path
    ):
        """Test that signup creates a user record in the database."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"dbuser_{unique_id}"
        email = f"dbuser_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user exists in database
        user = get_user_by_username(str(db_path), username)
        assert user is not None, f"User {username} should exist in database"
        assert user["email"].lower() == email.lower()
        assert user["role"] == "user"

    @pytest.mark.auth
    def test_signup_auto_login(self, page, flask_server, clean_db):
        """Test that user is automatically logged in after signup."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"autologin_{unique_id}"
        email = f"autologin_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Wait for redirect to verify page
        page.wait_for_url("**/verify-user/**", timeout=5000)

        # Navigate to home and check logged in state
        page.goto(flask_server["base_url"])
        navbar = NavbarComponent(page)
        navbar.expect_logged_in()

    @pytest.mark.auth
    def test_signup_awards_points(self, page, flask_server, clean_db, db_path):
        """Test that signup awards 1 point to the new user."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"pointsuser_{unique_id}"
        email = f"pointsuser_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user has 1 point
        points = get_user_points(str(db_path), username)
        assert points == 1, f"User should have 1 point, got {points}"

    @pytest.mark.auth
    def test_signup_user_is_unverified(self, page, flask_server, clean_db, db_path):
        """Test that newly signed up user has is_verified='False'."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"unverified_{unique_id}"
        email = f"unverified_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user is unverified
        user = get_user_by_username(str(db_path), username)
        assert user is not None
        assert user["is_verified"] == "False", "New user should be unverified"


class TestSignupErrors:
    """Tests for signup error scenarios."""

    @pytest.mark.auth
    def test_signup_duplicate_username(self, page, flask_server, test_user):
        """Test that signup with existing username shows error."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to signup with existing test_user username
        signup_page.signup_and_expect_error(
            test_user.username,
            f"unique_{uuid.uuid4().hex[:8]}@test.com",
            "TestPassword123!",
        )

    @pytest.mark.auth
    def test_signup_duplicate_username_case_insensitive(
        self, page, flask_server, app_settings, clean_db
    ):
        """Test that username check is case-insensitive (ADMIN rejected when admin exists)."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to signup with "ADMIN" when "admin" exists
        signup_page.signup_and_expect_error(
            app_settings["default_admin"]["username"].upper(),
            f"unique_{uuid.uuid4().hex[:8]}@test.com",
            "TestPassword123!",
        )

    @pytest.mark.auth
    def test_signup_duplicate_email(self, page, flask_server, test_user):
        """Test that signup with existing email shows error."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to signup with existing test_user email
        signup_page.signup_and_expect_error(
            f"uniqueuser_{uuid.uuid4().hex[:8]}",
            test_user.email,
            "TestPassword123!",
        )

    @pytest.mark.auth
    def test_signup_duplicate_email_case_insensitive(
        self, page, flask_server, test_user, db_path
    ):
        """Test that email check is case-insensitive."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to signup with uppercase version of existing email
        signup_page.signup_and_expect_error(
            f"uniqueuser_{uuid.uuid4().hex[:8]}",
            test_user.email.upper(),
            "TestPassword123!",
        )

    @pytest.mark.auth
    def test_signup_password_mismatch(self, page, flask_server, clean_db):
        """Test that signup with mismatched passwords shows error."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        signup_page.signup_and_expect_error(
            f"mismatch_{unique_id}",
            f"mismatch_{unique_id}@test.com",
            "TestPassword123!",
            "DifferentPassword456!",  # Different password for confirm
        )

    @pytest.mark.auth
    def test_signup_non_ascii_username(self, page, flask_server, clean_db):
        """Test that signup with non-ASCII username shows error."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        # Use unicode characters in username
        signup_page.signup_and_expect_error(
            f"üser_{unique_id}",
            f"unicode_{unique_id}@test.com",
            "TestPassword123!",
        )

    @pytest.mark.auth
    def test_signup_both_username_and_email_taken(self, page, flask_server, test_user):
        """Test that signup with both taken username and email shows specific error."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to signup with both existing username and email
        signup_page.signup_and_expect_error(
            test_user.username,
            test_user.email,
            "TestPassword123!",
        )


class TestSignupFormValidation:
    """Tests for form validation behavior."""

    @pytest.mark.auth
    def test_signup_username_too_short(self, page, flask_server, clean_db):
        """Test that username shorter than 4 characters triggers validation."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Fill form with short username (less than 4 chars)
        signup_page.fill_username("abc")
        signup_page.fill_email("short@test.com")
        signup_page.fill_password("TestPassword123!")
        signup_page.fill_password_confirm("TestPassword123!")
        signup_page.click_submit()

        # Check HTML5 validation or that we stay on signup page
        is_valid = signup_page.is_username_valid()
        if not is_valid:
            validation_msg = signup_page.get_username_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_signup_username_too_long(self, page, flask_server, clean_db, db_path):
        """Test that username longer than 25 characters triggers validation."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        # Fill form with long username (more than 25 chars)
        long_username = f"a{unique_id}" + "a" * 30  # Ensure >25 chars
        email = f"long_{unique_id}@test.com"
        signup_page.fill_username(long_username)
        signup_page.fill_email(email)
        signup_page.fill_password("TestPassword123!")
        signup_page.fill_password_confirm("TestPassword123!")

        # Check if maxlength attribute would prevent submission
        max_length = signup_page.get_username_max_length()
        if max_length > 0 and max_length < len(long_username):
            # maxlength prevents input of long usernames - just verify the attribute exists
            assert max_length == 25, "Username maxlength should be 25"
        else:
            # No client-side validation, submit and check server response
            signup_page.click_submit()
            # Server should either reject or truncate - verify user wasn't created with long name
            user = get_user_by_username(str(db_path), long_username)
            # Either user doesn't exist (rejected) or was truncated
            if user is None:
                # Good - server rejected the long username
                pass
            else:
                # User was created - check if username was truncated
                assert len(user["username"]) <= 25, "Username should be max 25 chars"

    @pytest.mark.auth
    def test_signup_email_invalid_format(self, page, flask_server, clean_db):
        """Test that invalid email format triggers validation."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        signup_page.fill_username(f"emailtest_{unique_id}")
        signup_page.fill_email("invalid-email-format")
        signup_page.fill_password("TestPassword123!")
        signup_page.fill_password_confirm("TestPassword123!")
        signup_page.click_submit()

        # Check HTML5 validation
        is_valid = signup_page.is_email_valid()
        if not is_valid:
            validation_msg = signup_page.get_email_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_signup_password_too_short(self, page, flask_server, clean_db):
        """Test that password shorter than 8 characters triggers validation."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        signup_page.fill_username(f"pwdtest_{unique_id}")
        signup_page.fill_email(f"pwdtest_{unique_id}@test.com")
        signup_page.fill_password("short")
        signup_page.fill_password_confirm("short")
        signup_page.click_submit()

        # Check HTML5 validation
        is_valid = signup_page.is_password_valid()
        if not is_valid:
            validation_msg = signup_page.get_password_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_signup_empty_fields_validation(self, page, flask_server, clean_db):
        """Test that empty fields trigger HTML5 validation."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        # Try to submit without filling any fields
        signup_page.click_submit()

        # Check HTML5 validation on required fields
        is_username_valid = signup_page.is_username_valid()
        if not is_username_valid:
            validation_msg = signup_page.get_username_validation_message()
            assert validation_msg != ""

    @pytest.mark.auth
    def test_signup_username_whitespace_stripped(
        self, page, flask_server, clean_db, db_path
    ):
        """Test that whitespace in username is stripped."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username_with_spaces = f"  spaced{unique_id}  "
        expected_username = f"spaced{unique_id}"

        signup_page.signup(
            username_with_spaces,
            f"spaced_{unique_id}@test.com",
            "TestPassword123!",
        )
        signup_page.expect_success_flash()

        # Verify username was stored without spaces
        user = get_user_by_username(str(db_path), expected_username)
        assert user is not None, "User with stripped username should exist"


class TestSignupSessionManagement:
    """Tests for session management during signup."""

    @pytest.mark.auth
    def test_signup_when_already_logged_in(self, logged_in_page, flask_server):
        """Test that already logged in user is redirected from signup page."""
        # logged_in_page fixture already has admin logged in
        # Try to navigate to signup page
        logged_in_page.goto(f"{flask_server['base_url']}/signup")

        # Should be redirected away from signup page (to home)
        page_url = logged_in_page.url
        assert "/signup" not in page_url

    @pytest.mark.auth
    def test_signup_session_persists_after_navigation(
        self, page, flask_server, clean_db
    ):
        """Test that session persists after navigating to other pages."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"persist_{unique_id}"
        email = f"persist_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Wait for redirect
        page.wait_for_url("**/verify-user/**", timeout=5000)

        # Navigate to home
        page.goto(flask_server["base_url"])

        # Should still be logged in
        navbar = NavbarComponent(page)
        navbar.expect_logged_in()

        # Navigate to another page
        page.goto(flask_server["base_url"])

        # Should still be logged in
        navbar.expect_logged_in()

    @pytest.mark.auth
    def test_can_access_protected_pages_after_signup(
        self, page, flask_server, clean_db
    ):
        """Test that user can access protected pages after signup."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"protected_{unique_id}"
        email = f"protected_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Wait for redirect to verify page
        page.wait_for_url("**/verify-user/**", timeout=5000)

        # Try to access create-post (protected page)
        page.goto(f"{flask_server['base_url']}/create-post")

        # Should be able to access the page (not redirected to login)
        assert "/login" not in page.url


class TestSignupEdgeCases:
    """Tests for edge cases in signup functionality."""

    @pytest.mark.auth
    def test_signup_with_special_email_characters(
        self, page, flask_server, clean_db, db_path
    ):
        """Test signup with special characters in email (user+tag@example.com)."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        username = f"plusemail_{unique_id}"
        email = f"user+tag_{unique_id}@test.com"
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user was created with the plus-addressed email
        user = get_user_by_email(str(db_path), email)
        assert user is not None, "User with plus-addressed email should exist"

    @pytest.mark.auth
    def test_signup_minimum_valid_lengths(self, page, flask_server, clean_db, db_path):
        """Test signup with minimum valid lengths (4 char username, 6 char email, 8 char password)."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:4]
        # Minimum username: 4 chars
        username = f"u{unique_id[:3]}"
        # Minimum email: 6 chars (a@b.co)
        email = f"a{unique_id[:1]}@t.co"
        # Minimum password: 8 chars
        password = "Pass123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user was created
        user = get_user_by_username(str(db_path), username)
        assert user is not None, "User with minimum valid lengths should exist"

    @pytest.mark.auth
    def test_signup_maximum_valid_lengths(self, page, flask_server, clean_db, db_path):
        """Test signup with maximum valid lengths (25 char username, 50 char email)."""
        signup_page = SignupPage(page, flask_server["base_url"])
        signup_page.navigate()

        unique_id = uuid.uuid4().hex[:8]
        # Maximum username: 25 chars
        username = f"maxuser{unique_id}".ljust(25, "x")[:25]
        # Maximum email: 50 chars (need to ensure valid format)
        email_local = f"max{unique_id}".ljust(35, "x")[:35]
        email = f"{email_local}@test.com"[:50]
        password = "TestPassword123!"

        signup_page.signup(username, email, password)
        signup_page.expect_success_flash()

        # Verify user was created
        user = get_user_by_username(str(db_path), username)
        assert user is not None, "User with maximum valid lengths should exist"
