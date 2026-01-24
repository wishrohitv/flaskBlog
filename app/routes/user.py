"""
This module contains the route for viewing user profiles.
"""

from flask import Blueprint, render_template
from sqlalchemy import func

from models import Comment, Post, User
from utils.log import Log

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/user/<username>")
def user(username):
    username_lower = username.lower()

    user = User.query.filter(
        func.lower(User.username) == username_lower
    ).first()

    if user:
        Log.success(f'User: "{username}" found')

        posts = Post.query.filter_by(author=user.username).order_by(
            Post.time_stamp.desc()
        ).all()

        views = sum(post.views or 0 for post in posts)

        comments = Comment.query.filter(
            func.lower(Comment.username) == username_lower
        ).all()

        show_posts = len(posts) > 0
        show_comments = len(comments) > 0

        Log.success(f'User: "{username}"s data loaded')

        user_tuple = (
            user.user_id, user.username, user.email, user.password,
            user.profile_picture, user.role, user.points,
            user.time_stamp, user.is_verified,
        )

        posts_tuples = [
            (
                p.id, p.title, p.tags, p.content, p.banner, p.author,
                p.views, p.time_stamp, p.last_edit_time_stamp,
                p.category, p.url_id, p.abstract,
            )
            for p in posts
        ]

        comments_tuples = [
            (c.id, c.post_id, c.comment, c.username, c.time_stamp)
            for c in comments
        ]

        return render_template(
            "user.html",
            user=user_tuple,
            views=views,
            posts=posts_tuples,
            comments=comments_tuples,
            show_posts=show_posts,
            show_comments=show_comments,
        )
    else:
        Log.error(f'User: "{username}" not found')
        return render_template("not_found.html")
