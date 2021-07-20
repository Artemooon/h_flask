from app import app
from flask_admin import Admin, form, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .models import db, Post, User, Role, FAQ, likes_users
from flask_login import LoginManager, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import redirect, url_for, request

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()



class BlogModelView(ModelView):

    # create_template = 'admin/edit-post.html'
    # edit_template = 'admin/edit-post.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    extra_js = ['https://cdn.ckeditor.com/4.16.1/standard/ckeditor.js']

    form_overrides = {
        'body': CKTextAreaField,
    }


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


admin = Admin(app, name='blog', index_view=HomeAdminView(name='Home'), url='/', template_mode='bootstrap4')

admin.add_view(BlogModelView(Post, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(FAQ, db.session))
# admin.add_view(ModelView(likes_users, db.session))
