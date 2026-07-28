from flask import Blueprint, request
from src.main import db
from http import HTTPStatus
from src.controllers.auth import Role

bp = Blueprint("role", __name__, url_prefix="/roles")

@bp.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created successfully"}, HTTPStatus.CREATED
     