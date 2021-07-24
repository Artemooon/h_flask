from flask.cli import FlaskGroup

from app import app
from app.models import db, User, Role, user_datastore
import sys
from flask_security.utils import hash_password
import os

cli = FlaskGroup(app)


@cli.command("createdb")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("createsuperuser")
def create_db():
    password = hash_password(os.getenv('SUPERUSER_PASS'))
    superuser = user_datastore.create_user(username='artem-root', email='artem.logachov773@gmail.com', password=password)
    db.session.commit()
    superuser_role = user_datastore.create_role(name="admin", description="administrator")
    user_datastore.create_role(name="moder", description="moderator")
    db.session.commit()
    user_datastore.add_role_to_user(superuser, superuser_role)
    db.session.commit()

if __name__ == "__main__":
    cli()
