from datetime import datetime
from ..db import get_db

db = get_db()
class Post(db.Model):
    
    __tablename__ = "post"

    id = db.Column(db.Integer,primary_key=True)
    # author_id = db.Column(db.Integer,unique=False,nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(50),nullable=False)
    body = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'