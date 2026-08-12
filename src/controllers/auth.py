from datetime import datetime
from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from flask_jwt_extended import JWTManager




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


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)

jwt = JWTManager()



class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f'Role(id={self.id!r}, name={self.name!r})'


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(80), unique=True)
    password: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('role.id'), nullable=True)
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r}, active={self.active!r})'

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    author_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})'