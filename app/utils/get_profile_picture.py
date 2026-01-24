from sqlalchemy import func

from models import User
from utils.log import Log


def get_profile_picture(username):
    """
    Returns the profile picture of the user with the specified username.

    Parameters:
        username (str): The username of the user whose profile picture is to be retrieved.

    Returns:
        str or None: The profile picture URL of the user, or None if not found.
    """
    user = User.query.filter(func.lower(User.username) == username.lower()).first()

    if user:
        profile_picture = user.profile_picture
        Log.info(f"Returning {username}'s profile picture: {profile_picture}")
        return profile_picture
    else:
        Log.error(f"Failed to retrieve profile picture for user: {username}")
        return None
