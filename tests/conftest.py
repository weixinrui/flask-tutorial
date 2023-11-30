import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from sqlalchemy import text
from data import users, posts

with open(os.path.join(os.path.dirname(__file__),'data.sql'), 'r',encoding='utf-8') as f:
    _data_sql = f.read()

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db(app)
        for user in users:
            try:
                get_db().session.add(user)
                get_db().session.commit()
            except:
                pass
        for post in posts:
            try:
                get_db().session.add(post)
                get_db().session.commit()
            except:
                pass
        

    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self,client) -> None:
        self._client = client
    
    def login(self, username='test',password='test'):
        return self._client.post(
            '/auth/login',
            data = {'username':username, 'password':password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)