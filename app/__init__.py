from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config.from_object("app.config.Config")

Session(app)

from app import views
from app import config
from app import models
from app import serializers
