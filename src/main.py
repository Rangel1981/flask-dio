from datetime import datetime
import os
import click

from flask import Flask, current_app
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
from sqlalchemy.orm import DeclarativeBase
from src.controllers.auth import db, jwt, Base, User, Post

migrate = Migrate()




@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()

    click.echo('Initialized the database.')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI= 'sqlite:///db.sqlite',
        JWT_SECRET_KEY='super-secret'
        )
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

   
   
    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #resgister blueprints
    from src.controllers import user, post, auth, role
    app.register_blueprint(user.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(role.bp)

    return app