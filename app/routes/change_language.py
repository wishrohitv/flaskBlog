from flask import Blueprint, render_template

change_language_blueprint = Blueprint("change_language", __name__)


@change_language_blueprint.route("/change-language")
def change_language():
    """
    This function is the route for the change language page.
    It is used to change the user's language.
    """

    return render_template("/change_language.html")
