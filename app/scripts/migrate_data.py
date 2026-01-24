#!/usr/bin/env python3
"""
One-time migration script from legacy SQLite databases to SQLAlchemy.

This script was used to migrate FlaskBlog from three separate SQLite databases
(users.db, posts.db, comments.db) to a unified SQLAlchemy-managed database.

Usage:
    cd /path/to/flaskBlog/app
    python scripts/migrate_data.py
"""

import os
import shutil
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

from settings import Settings

LEGACY_DB_FOLDER = "db/"
LEGACY_USERS_DB = LEGACY_DB_FOLDER + "users.db"
LEGACY_POSTS_DB = LEGACY_DB_FOLDER + "posts.db"
LEGACY_COMMENTS_DB = LEGACY_DB_FOLDER + "comments.db"


def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(LEGACY_DB_FOLDER, f"backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    for db_path in [LEGACY_USERS_DB, LEGACY_POSTS_DB, LEGACY_COMMENTS_DB]:
        if os.path.exists(db_path):
            filename = os.path.basename(db_path)
            backup_path = os.path.join(backup_dir, filename)
            shutil.copy2(db_path, backup_path)
            print(f"Backed up: {db_path} -> {backup_path}")

    return backup_dir


def get_legacy_users():
    if not os.path.exists(LEGACY_USERS_DB):
        return []

    conn = sqlite3.connect(LEGACY_USERS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT user_id, username, email, password, profile_picture, "
            "role, points, time_stamp, is_verified FROM users"
        )
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def get_legacy_posts():
    if not os.path.exists(LEGACY_POSTS_DB):
        return []

    conn = sqlite3.connect(LEGACY_POSTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, title, tags, content, banner, author, views, "
            "time_stamp, last_edit_time_stamp, category, url_id, abstract FROM posts"
        )
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def get_legacy_comments():
    if not os.path.exists(LEGACY_COMMENTS_DB):
        return []

    conn = sqlite3.connect(LEGACY_COMMENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, post_id, comment, username, time_stamp FROM comments")
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def migrate_data():
    print("=" * 60)
    print("FlaskBlog Database Migration")
    print("Legacy SQLite -> SQLAlchemy")
    print("=" * 60)

    legacy_exists = any(
        os.path.exists(db) for db in [LEGACY_USERS_DB, LEGACY_POSTS_DB, LEGACY_COMMENTS_DB]
    )

    if not legacy_exists:
        print("\nNo legacy databases found. Nothing to migrate.")
        return

    print("\n1. Creating backup...")
    backup_dir = create_backup()
    print(f"   Backup: {backup_dir}")

    print("\n2. Reading legacy data...")
    legacy_users = get_legacy_users()
    legacy_posts = get_legacy_posts()
    legacy_comments = get_legacy_comments()

    print(f"   Users: {len(legacy_users)}")
    print(f"   Posts: {len(legacy_posts)}")
    print(f"   Comments: {len(legacy_comments)}")

    if not any([legacy_users, legacy_posts, legacy_comments]):
        print("\nNo data to migrate.")
        return

    print("\n3. Initializing SQLAlchemy database...")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from database import db
    from models import Comment, Post, User

    db.init_app(app)

    with app.app_context():
        db.create_all()

        print("\n4. Migrating users...")
        users_migrated = 0
        for user_data in legacy_users:
            (user_id, username, email, password, profile_picture,
             role, points, time_stamp, is_verified) = user_data

            if User.query.filter_by(username=username).first():
                continue

            user = User(
                username=username, email=email, password=password,
                profile_picture=profile_picture, role=role, points=points,
                time_stamp=time_stamp, is_verified=is_verified,
            )
            db.session.add(user)
            users_migrated += 1

        db.session.commit()
        print(f"   Migrated: {users_migrated}")

        print("\n5. Migrating posts...")
        posts_migrated = 0
        post_id_mapping = {}

        for post_data in legacy_posts:
            (old_id, title, tags, content, banner, author, views,
             time_stamp, last_edit_time_stamp, category, url_id, abstract) = post_data

            existing = Post.query.filter_by(url_id=url_id).first()
            if existing:
                post_id_mapping[old_id] = existing.id
                continue

            post = Post(
                title=title, tags=tags, content=content,
                banner=banner if banner else b"", author=author,
                views=views or 0, time_stamp=time_stamp,
                last_edit_time_stamp=last_edit_time_stamp,
                category=category, url_id=url_id, abstract=abstract or "",
            )
            db.session.add(post)
            db.session.flush()
            post_id_mapping[old_id] = post.id
            posts_migrated += 1

        db.session.commit()
        print(f"   Migrated: {posts_migrated}")

        print("\n6. Migrating comments...")
        comments_migrated = 0

        for comment_data in legacy_comments:
            old_id, old_post_id, comment_text, username, time_stamp = comment_data

            new_post_id = post_id_mapping.get(old_post_id)
            if new_post_id is None:
                continue

            comment = Comment(
                post_id=new_post_id, comment=comment_text,
                username=username, time_stamp=time_stamp,
            )
            db.session.add(comment)
            comments_migrated += 1

        db.session.commit()
        print(f"   Migrated: {comments_migrated}")

    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    migrate_data()
