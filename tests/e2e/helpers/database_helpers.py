"""
Database helper functions for E2E tests.
"""

import sqlite3

from passlib.hash import sha512_crypt as encryption


def get_db_connection(db_path: str):
    """Create a database connection."""
    return sqlite3.connect(db_path)


def reset_database(db_path: str):
    """
    Reset database to known state.
    Removes all test users (keeps admin), clears posts and comments created by test users.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        # Delete all users except the default admin
        cursor.execute("DELETE FROM users WHERE username != 'admin'")

        # Reset admin points to 0
        cursor.execute("UPDATE users SET points = 0 WHERE username = 'admin'")

        # Delete test posts (posts by users other than admin)
        cursor.execute("DELETE FROM posts WHERE author != 'admin'")

        # Delete test comments (comments by users other than admin)
        cursor.execute("DELETE FROM comments WHERE username != 'admin'")

        conn.commit()
    finally:
        conn.close()


def create_test_user(
    db_path: str,
    username: str,
    email: str,
    password: str,
    role: str = "user",
    is_verified: str = "True",
    points: int = 0,
) -> int:
    """
    Create a test user in the database.
    Returns the user_id of the created user.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        hashed_password = encryption.hash(password)
        profile_picture = (
            f"https://api.dicebear.com/7.x/identicon/svg?seed={username}&radius=10"
        )

        cursor.execute(
            """
            INSERT INTO users (username, email, password, profile_picture, role, points, is_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                email,
                hashed_password,
                profile_picture,
                role,
                points,
                is_verified,
            ),
        )

        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_user_by_username(db_path: str, username: str) -> dict | None:
    """
    Get user data by username.
    Returns a dictionary with user fields or None if not found.
    """
    conn = get_db_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(username) = LOWER(?)",
            (username,),
        )
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def delete_user(db_path: str, username: str) -> bool:
    """
    Delete a user by username.
    Returns True if user was deleted, False if not found.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM users WHERE LOWER(username) = LOWER(?)", (username,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def user_exists(db_path: str, username: str) -> bool:
    """Check if a user exists by username."""
    return get_user_by_username(db_path, username) is not None


def get_user_count(db_path: str) -> int:
    """Get the total number of users in the database."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_user_by_email(db_path: str, email: str) -> dict | None:
    """
    Get user data by email.
    Returns a dictionary with user fields or None if not found.
    """
    conn = get_db_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(email) = LOWER(?)",
            (email,),
        )
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def get_user_points(db_path: str, username: str) -> int | None:
    """
    Get user points by username.
    Returns the points value or None if user not found.
    """
    user = get_user_by_username(db_path, username)
    if user:
        return user.get("points", 0)
    return None


def email_exists(db_path: str, email: str) -> bool:
    """Check if an email exists in the database."""
    return get_user_by_email(db_path, email) is not None
