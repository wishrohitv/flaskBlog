from database import db
from models import User
from utils.log import Log


def add_points(points, user):
    """
    Adds the specified number of points to the user with the specified username.
    """
    user_obj = User.query.filter_by(username=user).first()

    if user_obj:
        user_obj.points = (user_obj.points or 0) + points
        db.session.commit()
        Log.info(f'{points} points added to "{user}"')
    else:
        Log.error(f'User "{user}" not found for adding points')
