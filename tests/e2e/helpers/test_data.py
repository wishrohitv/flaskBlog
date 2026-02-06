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
    def unverified(cls) -> "UserData":
        """Generate unverified user data."""
        return cls(is_verified="False")
