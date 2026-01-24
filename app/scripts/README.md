# Scripts

## migrate_data.py

Migration script for upgrading FlaskBlog from raw SQLite to SQLAlchemy.

### When to use

If you're upgrading FlaskBlog to the latest version on your deployment, you need to run this script to migrate your existing data.

### What it does

Migrates data from three legacy databases:
- `db/users.db` -> `users` table
- `db/posts.db` -> `posts` table
- `db/comments.db` -> `comments` table

Into a single SQLAlchemy-managed database (`instance/flaskblog.db`).

### Usage

```bash
cd /path/to/flaskBlog/app
uv run python scripts/migrate_data.py
```

### After migration

1. Start the app and verify everything works correctly
2. Test login, creating posts, comments, etc.
3. If everything is working, you can safely delete the `db/` folder and its backups
