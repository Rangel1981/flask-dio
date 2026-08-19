from src.models import db, User
from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from flask_jwt_extended import JWTManager



jwt = JWTManager()
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user or password != user.password:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK

