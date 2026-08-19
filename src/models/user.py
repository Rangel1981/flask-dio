from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db
import sqlalchemy as sa



class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(80), unique=True)
    password: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('role.id'), nullable=True)
    role: Mapped["role.Role"] = relationship(back_populates="users") # type: ignore

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r}, active={self.active!r})'
