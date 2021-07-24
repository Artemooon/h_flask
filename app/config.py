import os


# sudo lsof -i -P -n | grep 80

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "ur_#eadjm(edg$+$uw_=*gxbrb^cavep2cc$ncta%l67&_oj5e"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    FLASK_ADMIN_SWATCH = "cerulean"
    SECURITY_PASSWORD_SALT = "dshas23csa"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    CKEDITOR_HEIGHT = 550
    CKEDITOR_FILE_UPLOADER = 'upload'
    # UPLOADED_PATH = os.path.join(basedir, 'uploads')
    # SECURITY_LOGIN_USER_TEMPLATE = "login.html"
