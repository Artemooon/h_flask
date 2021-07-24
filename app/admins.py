from app import app
from flask_admin import Admin, form, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .models import db, Post, User, Role, FAQ, likes_users
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask import redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import validators
from flask_wtf import CSRFProtect
import os
import uuid
import random
from slugify import slugify

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['PREVIEW_UPLOAD_PATH'] = os.path.join(basedir, 'static/images/')
app.config['IMAGES_UPLOAD_PATH'] = os.path.join(basedir, 'static/images/articles')
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_ENABLE_CSRF'] = True

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

ckeditor = CKEditor(app)
csrf = CSRFProtect(app)

class BlogModelView(ModelView):

    create_template = 'admin/edit-post.html'
    edit_template = 'admin/edit-post.html'

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.has_role('admin') or current_user.has_role('moder'))

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    form_overrides = dict(body=CKEditorField)

    form_extra_fields = {
        'file': form.FileUploadField('Upload Preview Image', [validators.DataRequired()])
    }

    def on_model_change(self, form, model, is_created):
        if is_created and not model.slug:
            model.slug = slugify(model.title)

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)

                storage_file.save(
                    os.path.join(app.config['PREVIEW_UPLOAD_PATH'], path)
                )

                _form.preview_image_url.data = path

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(BlogModelView, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(BlogModelView, self).create_form(obj)
        )


class RoleModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.has_role('admin') or current_user.has_role('moder'))

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.has_role('admin')  or current_user.has_role('moder'))

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['IMAGES_UPLOAD_PATH']
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    unique_filename = str(uuid.uuid4())
    # f.filename = secure_filename(unique_filename + '.' + extension)
    f.save(os.path.join(app.config['IMAGES_UPLOAD_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)


admin = Admin(app, name='blog', index_view=HomeAdminView(name='Home'), url='/', template_mode='bootstrap4')

admin.add_view(BlogModelView(Post, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(ModelView(FAQ, db.session))
# admin.add_view(ModelView(likes_users, db.session))
