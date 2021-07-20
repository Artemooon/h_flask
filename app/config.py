import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dsduux83zao"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    FLASK_ADMIN_SWATCH = "cerulean"
    SECURITY_PASSWORD_SALT = "dshas23csa"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    # SECURITY_LOGIN_USER_TEMPLATE = "login.html"
