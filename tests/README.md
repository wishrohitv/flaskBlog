# Tests

End-to-end tests for Flask Blog using Pytest and Playwright.

## Quick Start

```bash
cd app

# Install test dependencies
uv sync --extra test
uv run playwright install chromium

# Run all tests (parallel by default)
uv run pytest ../tests/e2e/ -v

# Run specific test file
uv run pytest ../tests/e2e/auth/test_login.py -v

# Run with headed browser (visible)
uv run pytest ../tests/e2e/ --headed

# Run specific test class
uv run pytest ../tests/e2e/auth/test_login.py::TestLoginSuccess -v
```

## Parallel Execution

Tests run in parallel by default using `pytest-xdist` with automatic worker detection (`-n auto`). This uses all available CPU cores to speed up test execution.

```bash
# Run with specific number of workers
uv run pytest ../tests/e2e/ -n 4

# Run sequentially (disable parallel)
uv run pytest ../tests/e2e/ -n 0

# Run with slow motion for debugging (milliseconds)
uv run pytest ../tests/e2e/ --slowmo 500
```

**How it works:**

- A single Flask server is shared across all workers (coordinated via file locks)
- Each test creates unique users with UUIDs to avoid conflicts
- Database is backed up before tests and restored after all workers complete
- Browser contexts are isolated per test for clean state

## Structure

```
tests/
├── conftest.py                 # Root fixtures
└── e2e/
    ├── conftest.py             # E2E fixtures (server, browser, database)
    ├── auth/                   # Authentication tests
    │   ├── test_login.py
    │   ├── test_logout.py
    │   └── test_signup.py
    ├── pages/                  # Page Object Model
    │   ├── base_page.py
    │   ├── login_page.py
    │   ├── signup_page.py
    │   └── navbar_component.py
    └── helpers/                # Utilities
        ├── database_helpers.py
        └── test_data.py
```

## Test Coverage

### Authentication (`e2e/auth/`)

#### Login (`test_login.py` - 18 tests)

| Category        | Test                                         | Description                                    |
| --------------- | -------------------------------------------- | ---------------------------------------------- |
| Page Rendering  | `test_login_page_renders`                    | Page loads with all required elements          |
|                 | `test_login_page_has_csrf_token`             | CSRF protection enabled                        |
|                 | `test_login_page_has_forgot_password_link`   | Forgot password link present                   |
|                 | `test_login_page_title`                      | Correct page title                             |
| Success Flows   | `test_login_with_valid_credentials`          | Admin login with valid credentials             |
|                 | `test_login_redirect_after_success`          | Redirects to home after login                  |
|                 | `test_login_case_insensitive_username`       | Username is case-insensitive                   |
|                 | `test_login_whitespace_trimmed`              | Whitespace in username trimmed                 |
| Error Handling  | `test_login_wrong_password`                  | Wrong password shows error                     |
|                 | `test_login_nonexistent_user`                | Nonexistent user shows error                   |
|                 | `test_login_empty_password`                  | Empty password validation                      |
| Session         | `test_login_already_logged_in_redirects`     | Logged-in user redirected from login page      |
|                 | `test_login_creates_session`                 | Session created (navbar shows logged-in state) |
|                 | `test_session_persists_after_navigation`     | Session persists across pages                  |
| Form Validation | `test_login_empty_username_validation`       | HTML5 validation for empty username            |
|                 | `test_login_empty_password_validation`       | HTML5 validation for empty password            |
|                 | `test_login_form_prevents_double_submission` | No double submission issues                    |
| Dynamic Users   | `test_login_with_test_user`                  | Dynamic test user can login                    |
|                 | `test_login_test_user_creates_session`       | Test user login creates session                |

#### Logout (`test_logout.py` - 15 tests)

| Category      | Test                                             | Description                       |
| ------------- | ------------------------------------------------ | --------------------------------- |
| Basic         | `test_logout_clears_session_and_redirects`       | Logout redirects to home          |
|               | `test_logout_shows_success_flash_message`        | Success flash after logout        |
|               | `test_logout_button_not_visible_when_logged_out` | Logout hidden when not logged in  |
| Session State | `test_logout_removes_session_navbar_shows_login` | Navbar shows login after logout   |
|               | `test_logout_session_does_not_persist`           | Session cleared after navigation  |
|               | `test_cannot_access_create_post_after_logout`    | Protected pages redirect to login |
| Edge Cases    | `test_logout_when_not_logged_in_redirects`       | Direct /logout redirects to home  |
|               | `test_logout_when_not_logged_in_no_flash`        | No flash when not logged in       |
|               | `test_double_logout_does_not_error`              | Double logout is safe             |
| User Types    | `test_logout_admin_user`                         | Admin can logout                  |
|               | `test_logout_regular_user`                       | Regular user can logout           |
|               | `test_logout_and_login_as_different_user`        | Can switch users after logout     |
| UI Behavior   | `test_login_link_appears_after_logout`           | Login link visible after logout   |
|               | `test_profile_avatar_hidden_after_logout`        | Avatar hidden after logout        |
|               | `test_create_post_button_hidden_after_logout`    | Create post hidden after logout   |

#### Signup (`test_signup.py` - 22 tests)

| Category        | Test                                              | Description                               |
| --------------- | ------------------------------------------------- | ----------------------------------------- |
| Page Rendering  | `test_signup_page_renders`                        | Page loads with all elements              |
|                 | `test_signup_page_has_csrf_token`                 | CSRF protection enabled                   |
|                 | `test_signup_page_has_privacy_policy_link`        | Privacy policy link present               |
|                 | `test_signup_page_title`                          | Correct page title                        |
| Success Flows   | `test_signup_with_valid_data`                     | User can signup with valid data           |
|                 | `test_signup_creates_user_in_database`            | User record created in DB                 |
|                 | `test_signup_auto_login`                          | User auto-logged in after signup          |
|                 | `test_signup_awards_points`                       | 1 point awarded to new user               |
|                 | `test_signup_user_is_unverified`                  | New user has is_verified='False'          |
| Error Handling  | `test_signup_duplicate_username`                  | Existing username rejected                |
|                 | `test_signup_duplicate_username_case_insensitive` | Case-insensitive username check           |
|                 | `test_signup_duplicate_email`                     | Existing email rejected                   |
|                 | `test_signup_duplicate_email_case_insensitive`    | Case-insensitive email check              |
|                 | `test_signup_password_mismatch`                   | Mismatched passwords rejected             |
|                 | `test_signup_non_ascii_username`                  | Non-ASCII username rejected               |
|                 | `test_signup_both_username_and_email_taken`       | Both taken shows error                    |
| Form Validation | `test_signup_username_too_short`                  | Username < 4 chars rejected               |
|                 | `test_signup_username_too_long`                   | Username > 25 chars rejected              |
|                 | `test_signup_email_invalid_format`                | Invalid email format rejected             |
|                 | `test_signup_password_too_short`                  | Password < 8 chars rejected               |
|                 | `test_signup_empty_fields_validation`             | Empty fields trigger validation           |
|                 | `test_signup_username_whitespace_stripped`        | Whitespace stripped from username         |
| Session         | `test_signup_when_already_logged_in`              | Logged-in user redirected from signup     |
|                 | `test_signup_session_persists_after_navigation`   | Session persists after signup             |
|                 | `test_can_access_protected_pages_after_signup`    | Can access protected pages after signup   |
| Edge Cases      | `test_signup_with_special_email_characters`       | Plus-addressed email (user+tag@) accepted |
|                 | `test_signup_minimum_valid_lengths`               | Minimum valid lengths work                |
|                 | `test_signup_maximum_valid_lengths`               | Maximum valid lengths work                |

## Architecture

### Page Object Model

Pages encapsulate UI interactions:

```python
from tests.e2e.pages.login_page import LoginPage

def test_login(page, flask_server):
    login_page = LoginPage(page, flask_server["base_url"])
    login_page.navigate()
    login_page.login("admin", "admin")
    login_page.expect_success_flash()
```

### Fixtures

| Fixture            | Scope    | Purpose                          |
| ------------------ | -------- | -------------------------------- |
| `flask_server`     | session  | Starts/stops the Flask app       |
| `browser_instance` | session  | Single Chromium instance         |
| `clean_db`         | session  | Resets database once at start    |
| `page`             | function | Fresh page per test              |
| `test_user`        | function | Creates a unique UUID-based user |
| `logged_in_page`   | function | Pre-authenticated page           |

### Test Data

Generate test users with `UserData`:

```python
from tests.e2e.helpers.test_data import UserData

user = UserData.generate()           # Random user
admin = UserData.admin()             # Admin user
unverified = UserData.unverified()   # Unverified user
```

### Database Helpers

Direct database access for test setup:

```python
from tests.e2e.helpers.database_helpers import create_test_user, user_exists

create_test_user(db_path, "testuser", "test@example.com", "Password123!")
assert user_exists(db_path, "testuser")
```

## Markers

Run tests by category:

```bash
pytest -m auth      # Authentication tests
pytest -m smoke     # Quick smoke tests
pytest -m admin     # Admin-related tests
pytest -m slow      # Long-running tests
```

## CI/CD

Tests run automatically via GitHub Actions on:

- Push to `main`
- Pull requests

See `.github/workflows/e2e-tests.yml` for configuration.
