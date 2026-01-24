from models import Post
from utils.log import Log


def get_post_url_id_from_post(post_id: int):
    """
    Returns the post's url_id from post's id.
    Args:
        post_id (int): The post's primary key/id whose url_id to be retrieved.

    Returns:
        str or None: The post's url_id of the post, or None if not found.
    """
    post = Post.query.get(post_id)

    if post:
        url_id = post.url_id
        Log.info(f"Returning post's id {post_id} and post's url_id: {url_id}")
        return url_id
    else:
        Log.error(f"Failed to retrieve post's url_id for post id : {post_id}")
        return None
