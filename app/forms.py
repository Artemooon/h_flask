from wtforms import Form, StringField, PasswordField, validators


# Форма регистрации
class RegisterForm(Form):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Подтвердите пароль')


# Форма авторизации
class LoginForm(Form):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=30)])
    password = PasswordField('Пароль', [
        validators.DataRequired(), ])

