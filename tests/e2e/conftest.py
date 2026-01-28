"""
E2E test fixtures for Flask Blog application.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

# Add app directory to path for imports
APP_DIR = Path(__file__).parent.parent.parent / "app"
sys.path.insert(0, str(APP_DIR))


@pytest.fixture(scope="session")
def app_dir():
    """Return the app directory path."""
    return APP_DIR


@pytest.fixture(scope="session")
def db_path(app_dir):
    """Return the database file path."""
    return app_dir / "instance" / "flaskblog.db"


@pytest.fixture(scope="session")
def flask_server(app_settings, app_dir):
    """
    Session-scoped fixture that starts the Flask server.
    The server runs for the entire test session and is cleaned up at the end.
    """
    base_url = app_settings["base_url"]
    port = app_settings["port"]

    # Start the Flask application
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # Redirect output to devnull to prevent buffer filling and blocking
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=str(app_dir),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server to be ready
    max_wait = 30
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < max_wait:
        try:
            import urllib.request

            urllib.request.urlopen(base_url, timeout=1)
            server_ready = True
            break
        except Exception:
            time.sleep(0.5)

    if not server_ready:
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError(
            f"Flask server failed to start within {max_wait} seconds. "
            f"Check that port {port} is available and the app starts correctly."
        )

    yield {"process": process, "base_url": base_url, "port": port}

    # Cleanup: terminate the server
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


@pytest.fixture(scope="session")
def browser_instance(request):
    """Session-scoped browser instance to avoid repeated browser launches."""
    # Check if --headed flag was passed
    headed = request.config.getoption("--headed", default=False)
    slowmo = request.config.getoption("--slowmo", default=0)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed, slow_mo=slowmo)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance, flask_server):
    """
    Function-scoped browser context for test isolation.
    Each test gets a fresh context with clean cookies/storage.
    """
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 720},
        base_url=flask_server["base_url"],
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Function-scoped page for each test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session", autouse=True)
def backup_and_restore_db(db_path):
    """
    Session-scoped fixture that backs up the database before tests
    and restores it after all tests complete.
    """
    backup_path = db_path.with_suffix(".db.bak")

    # Create backup before any tests run
    if db_path.exists():
        shutil.copy2(db_path, backup_path)

    yield

    # Restore backup after all tests complete
    if backup_path.exists():
        shutil.copy2(backup_path, db_path)
        backup_path.unlink()  # Remove the backup file


@pytest.fixture(scope="function")
def clean_db(db_path):
    """
    Reset database to known state before each test.
    Removes test users but keeps the admin.
    """
    from tests.e2e.helpers.database_helpers import reset_database

    reset_database(str(db_path))
    yield


@pytest.fixture(scope="function")
def logged_in_page(page, flask_server, app_settings):
    """
    Page fixture with admin already logged in.
    Useful for tests that require authenticated state.
    """
    from tests.e2e.pages.login_page import LoginPage

    login_page = LoginPage(page, flask_server["base_url"])
    login_page.navigate("/login/redirect=&")
    login_page.login(
        app_settings["default_admin"]["username"],
        app_settings["default_admin"]["password"],
    )

    # Wait for redirect after login
    page.wait_for_url("**/", timeout=5000)

    yield page


@pytest.fixture(scope="function")
def test_user(clean_db, db_path):
    """
    Create a test user and return credentials.
    The user is created fresh for each test.
    """
    from tests.e2e.helpers.database_helpers import create_test_user
    from tests.e2e.helpers.test_data import UserData

    user_data = UserData.generate()
    create_test_user(
        db_path=str(db_path),
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
    )

    return user_data


@pytest.fixture(scope="function")
def unverified_test_user(clean_db, db_path):
    """
    Create an unverified test user and return credentials.
    The user is created fresh for each test with is_verified="False".
    """
    from tests.e2e.helpers.database_helpers import create_test_user
    from tests.e2e.helpers.test_data import UserData

    user_data = UserData.unverified()
    create_test_user(
        db_path=str(db_path),
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
        is_verified=user_data.is_verified,
    )

    return user_data
