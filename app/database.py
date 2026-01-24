from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha512_crypt as encryption

from settings import Settings
from utils.log import Log
from utils.time import current_time_stamp

db = SQLAlchemy()


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = Settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Settings.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    with app.app_context():
        db.create_all()
        Log.success("Database tables created/verified")
        _create_default_admin()


def _create_default_admin():
    if not Settings.DEFAULT_ADMIN:
        return

    from models import User

    existing_admin = User.query.filter_by(username=Settings.DEFAULT_ADMIN_USERNAME).first()

    if existing_admin:
        Log.info(f'Admin: "{Settings.DEFAULT_ADMIN_USERNAME}" already exists')
        return

    admin = User(
        username=Settings.DEFAULT_ADMIN_USERNAME,
        email=Settings.DEFAULT_ADMIN_EMAIL,
        password=encryption.hash(Settings.DEFAULT_ADMIN_PASSWORD),
        profile_picture=Settings.DEFAULT_ADMIN_PROFILE_PICTURE,
        role="admin",
        points=Settings.DEFAULT_ADMIN_POINT,
        time_stamp=current_time_stamp(),
        is_verified="True",
    )

    db.session.add(admin)
    db.session.commit()

    Log.success(
        f'Admin: "{Settings.DEFAULT_ADMIN_USERNAME}" added to database as initial admin',
    )
