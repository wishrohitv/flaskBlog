"""
Test data factories and constants for E2E tests.
"""

import uuid
from dataclasses import dataclass, field


@dataclass
class UserData:
    """Test user data with default values."""

    username: str = field(default_factory=lambda: f"testuser_{uuid.uuid4().hex[:8]}")
    email: str = field(default_factory=lambda: f"test_{uuid.uuid4().hex[:8]}@test.com")
    password: str = "TestPassword123!"
    role: str = "user"
    is_verified: str = "True"

    @classmethod
    def generate(cls, **overrides) -> "UserData":
        """Generate test user data with optional overrides."""
        return cls(**overrides)

    @classmethod
    def admin(cls) -> "UserData":
        """Generate admin user data."""
        return cls(
            username=f"testadmin_{uuid.uuid4().hex[:8]}",
            email=f"admin_{uuid.uuid4().hex[:8]}@test.com",
            role="admin",
        )

    @classmethod
    def unverified(cls) -> "UserData":
        """Generate unverified user data."""
        return cls(is_verified="False")


@dataclass
class PostData:
    """Test post data with default values."""

    title: str = field(default_factory=lambda: f"Test Post {uuid.uuid4().hex[:8]}")
    content: str = "This is test content for the post."
    category: str = "test"
    tags: str = "test,automation"
    abstract: str = "Test post abstract"
    url_id: str = field(default_factory=lambda: f"test-post-{uuid.uuid4().hex[:8]}")
    author: str = "admin"

    @classmethod
    def generate(cls, **overrides) -> "PostData":
        """Generate test post data with optional overrides."""
        return cls(**overrides)


# Invalid username test cases
INVALID_USERNAMES = [
    "",  # Empty
    " ",  # Whitespace only
    "a" * 256,  # Too long
    "user@name",  # Invalid character
    "user<script>",  # XSS attempt
]

# Invalid password test cases
INVALID_PASSWORDS = [
    "",  # Empty
    " ",  # Whitespace only
    "a",  # Too short (single char)
]

# Default admin credentials (from Settings)
DEFAULT_ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "admin",
    "email": "admin@flaskblog.com",
}

# Test constants
TEST_TIMEOUT = 5000  # Default timeout in milliseconds
SLOW_TEST_TIMEOUT = 15000  # Timeout for slow tests
