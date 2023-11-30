from datetime import datetime
from flaskr.models import User
from flaskr.models import Post
from flaskr.db import get_db

users = [
    User(username='test',password='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    User(username='other',password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f790')
]

posts = [
    Post(title='test title',body='test\nbody',author_id=1,created=datetime.strptime('2018-01-01 00:00:00','%Y-%m-%d %H:%M:%S'))
]