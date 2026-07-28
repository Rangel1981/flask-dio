from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from src.main import db
from src.controllers.auth import User
from functools import wraps

def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user.id = get_jwt_identity()
            user = db.session.execute(db.select(User).where(User.username == user.id)).scalar()
            if user.role.name != role_name:
                return {"message": "User dont have permission"}, HTTPStatus.FORBIDDEN

            return f(*args, **kwargs)

        return wrapped

    return decorator