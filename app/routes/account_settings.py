from flask import Blueprint, redirect, render_template, request, session

from models import User
from utils.delete import delete_user
from utils.log import Log

account_settings_blueprint = Blueprint("account_settings", __name__)


@account_settings_blueprint.route("/account-settings", methods=["GET", "POST"])
def account_settings():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()

        if not user:
            return redirect("/")

        if request.method == "POST":
            delete_user(user.username)
            return redirect("/")

        return render_template(
            "account_settings.html",
            user=(user.username,),
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach account settings without being logged in"
        )

        return redirect("/login/redirect=&account-settings")
