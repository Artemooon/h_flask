from flask_sqlalchemy import SQLAlchemy
from app import app
import datetime

db = SQLAlchemy(app)


class Post(db.Model):
    # __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body
