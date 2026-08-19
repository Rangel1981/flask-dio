from flask import Blueprint, request
from src.models import Post, db
from http import HTTPStatus
from sqlalchemy import inspect
 


bp = Blueprint("post", __name__, url_prefix="/posts")

def _create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [{"id": post.id, "title": post.title, "body": post.body, "author_id": post.author_id} for post in posts]

@bp.route("/", methods=["GET", "POST"])
def handler_posts():
    if request.method == "POST":
        _create_post()
        return {"message": "Post created successfully"}, HTTPStatus.CREATED
    else:
        return {"posts": _list_posts()}, HTTPStatus.OK
    
@bp.route("/<int:post_id>")
def _get_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    return {"id": post.id, "title": post.title, "body": post.body, "author_id": post.author_id}


@bp.route("/author/<int:author_id>", methods=["GET"])
def get_post_id_user(author_id: int):
    query = db.select(Post).filter_by(author_id=author_id)
    posts = db.session.execute(query).scalars()
    
    return [
        {
            "id": post.id, 
            "title": post.title, 
            "body": post.body, 
            "author_id": post.author_id
        } 
        for post in posts
    ]
@bp.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
        db.session.commit()

    return {"id": post.id, "title": post.title, "body": post.body, "author_id": post.author_id}

@bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return " ", HTTPStatus.NO_CONTENT