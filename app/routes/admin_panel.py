from flask import Blueprint, redirect, render_template, request, session

from models import User
from utils.log import Log

admin_panel_blueprint = Blueprint("admin_panel", __name__)


@admin_panel_blueprint.route("/admin")
def admin_panel():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()

        if not user:
            return redirect("/")

        if user.role == "admin":
            Log.info(f"Admin: {session['username']} reached to the admin panel")

            Log.info("Rendering admin_panel.html: params: None")

            return render_template("admin_panel.html")
        else:
            Log.error(
                f"{request.remote_addr} tried to reach admin panel without being admin"
            )

            return redirect("/")
    else:
        Log.error(f"{request.remote_addr} tried to reach admin panel being logged in")

        return redirect("/")
