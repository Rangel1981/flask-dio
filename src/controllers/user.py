from flask import Blueprint, request
from src.controllers.auth import db, User
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from src.utils import requires_role

bp = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
                username=data["username"], 
                password=data["password"],
                role_id=data.get("role_id")
            )
    db.session.add(user)
    db.session.commit()
   
def _list_useres():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [{"id": user.id, 
             "username": user.username,
             "role_id": 
                {"id": user.role_id, 
                 "name": user.role.name}
            if user.role else None} for user in users]


@bp.route("/", methods=["GET" , "POST"])
@jwt_required()
@requires_role("admin")
def handler_users():
    if request.method == "POST":
        _create_user()
        return {"message": "User created successfully"}, HTTPStatus.CREATED
    else:
        return {"users": _list_useres()}, HTTPStatus.OK

@bp.route("/<int:user_id>")    
def _get_user(user_id: int):
    user = db.get_or_404(User, user_id)
    return {"id": user.id, "username": user.username}

@bp.route("/<int:user_id>", methods=["PATCH"])    
def update_user(user_id: int):
    user = db.get_or_404(User, user_id)
    data = request.json
   
    mapper = inspect(User)
    for columnn in mapper.attrs:
        if columnn.key in data:
            setattr(user, columnn.key, data[columnn.key])
        db.session.commit()


    return {"id": user.id, "username": user.username}


@bp.route("/<int:user_id>", methods=["DELETE"] )    
def delete_user(user_id: int):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}