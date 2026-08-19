from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db
import sqlalchemy as sa
from datetime import datetime

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    author_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})'