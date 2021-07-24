import datetime
from app import app
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
                       db.Column('users_id', db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer(),
                                 db.ForeignKey('roles.id')))

likes_users = db.Table('likes_users',
                       db.Column('users_id', db.Integer(),
                                 db.ForeignKey('users.id', ondelete='CASCADE')),
                       db.Column('posts_id', db.Integer(),
                                 db.ForeignKey('posts.id', ondelete='CASCADE')))


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(180))

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.datetime.now)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('roles', passive_deletes=True, lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class FAQ(db.Model):
    __tablename__ = "faqs"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text(), nullable=False)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    author = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(120))
    preview_image_url = db.Column(db.Unicode(164), nullable=True)
    active = db.Column(db.Boolean())
    likes = db.relationship('User', secondary=likes_users, remote_side=id,
                            backref=db.backref('likes', lazy='dynamic'))
