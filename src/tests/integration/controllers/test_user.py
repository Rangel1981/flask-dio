from http import HTTPStatus
from sqlalchemy import func
from src.controllers.auth import Role, User, db


def test_get_user_success(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon", password="testtesttesttesttesttesttest", role_id=role.id)
    db.session.add(user)
    db.session.commit()


    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id, "username": user.username}


def test_get_user_not_found(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1 

    response = client.get(f'/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND



def test_create_user(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user = User(username="jhon", password="testtesttesttesttesttesttest", role_id=role.id)
    db.session.add(user)
    db.session.commit()


    response = client.post('/auth/login', json={'username': user.username, 'password': user.password})
    access_token = response.json.get('access_token')

    playlord = {"username": "user2", "password": "user2", "role_id": role.id}

    response = client.post('/users/', json=playlord, headers={'Authorization': f'Bearer {access_token}'})


    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created successfully"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2  




    
def test_get_user(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon", password="testtesttesttesttesttesttest", role_id=role.id)
    db.session.add(user)
    db.session.commit()


    response_login = client.post('/auth/login', json={'username': user.username, 'password': user.password})
    assert response_login.status_code == HTTPStatus.OK, f"Erro no Login ({response_login.status_code}): {response_login.json}"

    access_token = response_login.json.get('access_token')

    response = client.get('/users/', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == HTTPStatus.OK, f"Erro no GET /users/ ({response.status_code}): {response.json}"
    assert response.json == {
        "users": 
        [{
            "id": user.id, 
             "username": user.username,
             "role_id": 
                {"id": user.role_id, 
                 "name": user.role.name
                 }
            }
        ]
    }