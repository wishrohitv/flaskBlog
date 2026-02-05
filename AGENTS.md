# AGENTS.md

This file provides guidance to AI Agents when working with code in this repository.

## Development Commands

**Always use Make commands instead of manual commands.**

```bash
make help          # Show all available commands
make install       # Install all dependencies (app + dev + test + Playwright)
make install-app   # Install app dependencies only
make run           # Run the Flask application (http://localhost:1283)
make docker        # Build and run with Docker
make docker-build  # Build Docker image
make docker-run    # Run Docker container
make test          # Run E2E tests (parallel)
make test-slow     # Run tests with visible browser (slow-mo, sequential)
make lint          # Format and lint code (auto-fix)
make ci            # Run CI checks
make clean         # Remove cache files
```

Default admin credentials: admin / admin

## Architecture Overview

This is a Flask blog application using Flask-SQLAlchemy with SQLite. The main application code lives in the `app/` directory.

### Core Structure

- **app/app.py** - Application entry point, registers all blueprints and middleware
- **app/settings.py** - Configuration class with all app settings (Settings class)
- **app/models.py** - SQLAlchemy models: User, Post, Comment
- **app/database.py** - Database initialization and default admin creation

### Routes Organization

Routes are organized as Flask Blueprints in `app/routes/`. Each route file exports a blueprint that gets registered in `app.py`. Key patterns:

- Admin routes: `admin_panel.py`, `admin_panel_users.py`, `admin_panel_posts.py`, `admin_panel_comments.py`
- Auth routes: `login.py`, `signup.py`, `logout.py`, `verify_user.py`, `password_reset.py`
- User routes: `account_settings.py`, `change_password.py`, `change_username.py`, `change_profile_picture.py`
- Content routes: `post.py`, `create_post.py`, `edit_post.py`, `category.py`, `search.py`

### Utils Organization

Utility functions in `app/utils/` are grouped by purpose:

- **forms/** - WTForms form definitions (login_form.py, sign_up_form.py, etc.)
- **context_processor/** - Jinja2 context processors for templates
- **before_request/** - Request preprocessing middleware
- **error_handlers/** - Custom error handlers (404, 401, CSRF)

### Frontend Stack

- **Tailwind CSS v4** (via CDN browser build)
- **DaisyUI v5** for component styling (35+ themes available in Settings.THEMES)
- **Tabler Icons** for iconography
- Templates use Jinja2 with `app/templates/layout.html` as the base
- Reusable components in `app/templates/components/`

### Internationalization

Translations are JSON files in `app/translations/` (en, tr, es, de, zh, fr, uk, ru, pt, ja, pl, hi). Access translations in templates via `translations` context variable injected by `utils/context_processor/translations.py`.

### Database Models

- **User** - user_id, username, email, password (hashed), role (user/admin), points, is_verified
- **Post** - id, title, content, banner (binary), author, views, category, url_id, abstract, has `hot_score` hybrid property
- **Comment** - id, post_id (FK), comment, username, time_stamp

### Configuration

All settings in `app/settings.py` are read from environment variables via `os.environ.get()` with sensible defaults. A `.env` file in the project root is loaded automatically by `python-dotenv`. See `.env.example` for all available options.

Key settings: `APP_HOST`, `APP_PORT`, `DEBUG_MODE`, `SQLALCHEMY_DATABASE_URI`, `APP_SECRET_KEY`, `SMTP_*`, `DEFAULT_ADMIN_*`.

### Docker

- **Dockerfile** — Single-stage build using `ghcr.io/astral-sh/uv:python3.10-alpine`. Runs as non-root `flaskblog` user (UID 1000). Only production deps installed (`uv sync --frozen --no-dev --no-cache`).
- **.dockerignore** — Whitelist approach: excludes everything (`*`), then includes only `app/` minus non-runtime files (`.venv`, `__pycache__`, `.ruff_cache`, `scripts`, `log`).
- **Environment variables** — Not baked into the image. Passed at runtime via `docker run --env-file .env` (handled automatically by `make docker-run` if `.env` exists).
- **Example DB** — `app/instance/flaskblog.db` is included in the image so the app starts with sample data.
- **Ports** — Container binds to `0.0.0.0:1283` (overrides Flask's default `localhost` via `APP_HOST` env var).

### Key Conventions

- Passwords hashed with Passlib's sha512_crypt
- CSRF protection enabled via Flask-WTF
- Session-based authentication (check `session["userName"]`)
- Timestamps stored as Unix integers via `utils/time.py`
- Posts use `url_id` for URL-friendly slugs

### Testing

E2E tests using Pytest + Playwright in `tests/e2e/`. See [`tests/README.md`](tests/README.md) for details.

---

ultrathink
