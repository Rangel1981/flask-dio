import pytest
from src.main import create_app
from src.controllers.auth import db

@pytest.fixture()
def app():
    app = create_app({
            'SECRET_KEY': "sua-chave-secreta-super-segura-e-longa-com-32-caracteres",
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///',
            'JWT_SECRET_KEY':"sua-chave-secreta-super-segura-e-longa-com-32-caracteres"
            })
    
    with app.app_context():
        db.create_all()
        yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


