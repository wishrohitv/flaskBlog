# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

All commands should be run from the `app/` directory:

```bash
cd app

# Run the application
uv run app.py

# Run a specific script
uv run python scripts/migrate_data.py
```

The application runs at `http://localhost:1283` by default.

Default admin credentials: `admin` / `admin`

## Architecture Overview

FlaskBlog is a monolithic Flask application using the Blueprint pattern for route organization.

### Core Files (app/)

- **app.py** - Application entry point, registers blueprints, configures middleware (CSRF, CSP headers, error handlers, context processors)
- **settings.py** - Configuration class with all app settings (ports, features, SMTP, reCAPTCHA, themes, languages)
- **database.py** - SQLAlchemy initialization and default admin creation
- **models.py** - Three SQLAlchemy models: `User`, `Post`, `Comment`

### Route Organization (app/routes/)

Each feature has its own blueprint file. Major routes:

- Authentication: `login.py`, `signup.py`, `logout.py`, `verify_user.py`, `password_reset.py`
- Content: `post.py`, `create_post.py`, `edit_post.py`, `category.py`, `search.py`
- Admin: `admin_panel.py`, `admin_panel_users.py`, `admin_panel_posts.py`, `admin_panel_comments.py`
- User: `user.py`, `dashboard.py`, `account_settings.py`, `change_*.py`

### Utilities (app/utils/)

- **context_processor/** - Jinja template context functions (translations, user state, markdown)
- **before_request/** - Request preprocessing (browser language detection)
- **error_handlers/** - Custom 401, 404, CSRF error pages
- **forms/** - WTForms form definitions

### Database

- Uses Flask-SQLAlchemy with SQLite (`instance/flaskblog.db`)
- Passwords hashed with passlib (sha512_crypt)
- Migration script available: `scripts/migrate_data.py` for upgrading from legacy raw SQLite

### Frontend

- Templates use Jinja2 with `layout.html` as base template
- TailwindCSS via CDN, DaisyUI themes (35+ themes configurable in settings)
- Milkdown editor for post creation
- 12 supported languages with translations in `translations/`

### Key Patterns

- Feature toggles in `Settings` class control login, registration, reCAPTCHA, default admin
- Logging via Tamga logger (can be toggled with Werkzeug logger)
- Content Security Policy headers set in `after_request`
- Posts use URL slugs (`url_id` field) with hot score ranking algorithm
