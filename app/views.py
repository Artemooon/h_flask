import datetime
from app import app
from flask import request, render_template, redirect, flash, url_for, jsonify
from flask_security import login_user, current_user, logout_user, login_required
from flask_security.utils import hash_password

from .forms import RegisterForm, LoginForm
from .models import db, Post, User, FAQ, user_datastore


@app.route('/')
def index():
    all_posts = Post.query.filter_by(active=True).all()

    return render_template('index.html', posts=all_posts, current_user=current_user)


@app.route('/<string:slug>/favorite/', methods=(['GET']))
def favorite_articles(slug):
    return render_template('favorite-user.html')


@app.route('/article/<string:slug>/like/', methods=(['POST', 'GET']))
def like_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    is_liked = False
    if current_user in post.likes:
        post.likes.remove(current_user)
        db.session.commit()
        is_liked = False
    else:
        post.likes.append(current_user)
        db.session.commit()
        is_liked = True

    total_likes = len(post.likes)

    return jsonify(is_liked=is_liked, total_likes=total_likes)


@app.route('/article/<string:slug>', methods=(['GET']))
def post(slug):
    # Удаляем пост при помощи кнопки на главной странице
    post = Post.query.filter_by(slug=slug).first_or_404()
    is_liked = False

    if current_user in post.likes:
        is_liked = True

    total_likes = len(post.likes)

    return render_template('post.html', post=post, is_liked=is_liked, total_likes=total_likes)


@app.route('/faqs', methods=['GET'])
def faq():
    faq = FAQ.query.all()

    return render_template('faq.html', faqs=faq)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        username_val = request.form['username']
        result = User.query.filter_by(username=username_val).first()
        if result and username_val == result.username:
            flash("This username is already registered!", 'warning')
            return redirect(url_for('register'))

        email = request.form['email']
        result = User.query.filter_by(email=email).first()
        if result and email == result.email:
            flash("This email is already registered!", 'warning')
            return redirect(url_for('register'))

        else:
            username = form.username.data
            password = hash_password(form.password.data)
            email = form.email.data

            user_datastore.create_user(username=username, email=email, password=password)
            db.session.commit()

            return redirect(url_for('security.login'))

            flash('Вы успешно зарегестрировались. Теперь вы можете войти', 'success')

    return render_template('register.html', form=form)
