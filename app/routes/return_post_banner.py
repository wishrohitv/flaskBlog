from io import BytesIO

from flask import Blueprint, abort, request, send_file

from models import Post
from utils.log import Log

return_post_banner_blueprint = Blueprint("return_post_banner", __name__)


@return_post_banner_blueprint.route("/post-image/<int:post_id>")
def return_post_banner(post_id):
    """
    This function returns the banner image for a given post ID.

    Args:
        post_id (int): The ID of the post for which the banner image is requested.

    Returns:
        The banner image for the given post ID as a Flask Response object.

    """
    post = Post.query.get(post_id)

    if not post or not post.banner:
        abort(404)

    image = BytesIO(post.banner)

    Log.info(f"Post: {post_id} | Image: {request.base_url} loaded")

    return send_file(image, mimetype="image/png")
