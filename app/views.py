from app import app
from .models import db, Post
from .serializers import PostSerializer
import datetime
from flask import request, render_template, redirect, flash
from wtforms import Form, StringField, TextAreaField, validators


# Форма добавление и редактирования постов
class AddArticleForm(Form):
    title = StringField('Title', [validators.Length(min=3, max=120)])
    description = TextAreaField('Description', [validators.Length(min = 1, max = 500)])


@app.route('/')
def index():
    all_posts = Post.query.all()

    return render_template('index.html', posts=all_posts)


# Страница добавление постов, содержит в себе форму создания нового поста
@app.route('/add-post', methods=['POST'])
def add_post():
    post_serializer = PostSerializer()

    # Вытаскиваем данные из формы
    title = request.json['title']
    body = request.json['body']

    # Добавляем введенные данные в нашу таблицу
    new_post = Post(title, body)

    db.session.add(new_post)
    # Коммитим
    db.session.commit()

    # Редирект на главную страницу
    return post_serializer.jsonify(new_post)



# Страница для редактирования постов, содержит в себе форму редактирования поста ссылка принимает параметр id который указывает на id нашего поста в таблице
@app.route('/edit-post/<string:id>', methods=['POST', 'GET'])
def edit_post(id):
    # Получаем все данные определенного поста
    post_edit = Post.query.filter_by(id=id).first()

    # Таже самая форма
    form = AddArticleForm(request.form)

    # В placeholder формы добавляем значения title and description
    form.title.data = post_edit.title
    form.description.data = post_edit.body

    # Проверка на метод пост и на валидность введнных данных
    if request.method == 'POST' and form.validate():
        # Получаем данные из формы для редактирования постов
        title = request.form['title']
        body = request.form['description']

        # Обновляем наш пост
        post_edit.title = title
        post_edit.body = body
        db.session.commit()

        # Редирект на главную страницу
        return redirect('/')

    return render_template('edit-post.html', form=form)


"""Страница для удаления поста с определенным id,ссылка принимает параметр id который указывает на id нашего поста 
в таблице"""


@app.route('/delete-post/<string:id>', methods=(['POST', 'GET']))
def delete_post(id):
    post_delete = Post.query.filter_by(id=id).first()

    db.session.delete(post_delete)
    db.session.commit()

    # Вспоминаем про флеш 😥
    flash("You DELETE the post!", 'danger')

    return redirect('/')


@app.route('/post/<string:id>', methods=(['POST', 'GET']))
def post(id):
    # Удаляем пост при помощи кнопки на главной странице
    post = Post.query.filter_by(id=id).first()

    return render_template('post.html', post=post)