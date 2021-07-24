from flask import Flask
from flask_session import Session
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("app.config.Config")

login_manager = LoginManager()
login_manager.init_app(app)

Session(app)

from app import config
from app import admins
from app import views
from app import models
from app import tests

# if __name__ == "__main__":
#     app.run(debug=False)