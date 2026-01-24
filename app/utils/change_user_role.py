from flask import redirect, session
from sqlalchemy import func

from database import db
from models import User
from utils.log import Log


def change_user_role(username):
    """
    Changes the role of the user with the specified username.
    """
    user = User.query.filter(func.lower(User.username) == username.lower()).first()

    if not user:
        Log.error(f'User "{username}" not found')
        return

    new_role = "user" if user.role == "admin" else "admin"
    user.role = new_role
    db.session.commit()

    Log.success(
        f'Admin: "{session["username"]}" changed user: "{username}"s role to "{new_role}" ',
    )

    if session["username"].lower() == username.lower():
        Log.success(f'Admin: "{session["username"]}" changed his role to "user"')
        return redirect("/")
