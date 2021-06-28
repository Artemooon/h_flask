from flask import Flask, render_template, request,flash, redirect, url_for
from flask_session import Session
from wtforms import Form,StringField,TextAreaField,validators
import sqlite3
import datetime


app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)


#Описание создания таблицы постов находится в файле create_tables.py

# Форма добавление и редактирования постов
class AddArticleForm(Form):
    title = StringField('Title',[validators.Length(min = 3, max = 120)])
    description = TextAreaField('Description',[validators.Length(min = 1, max = 500)])


# Главная страница, содержит в себе все созданные посты и информацию про них
@app.route('/')
def index():
    # Подключение к бд
    con = sqlite3.connect("blog.db")
    # Курсор
    cur = con.cursor()
    
    # Выбираем все записи из таблицы с постами
    cur.execute("SELECT * FROM Posts")
    posts = cur.fetchall()
    
    # Закрываем соединение с бд
    con.close()
    return render_template('index.html',posts = posts)    


# Страница добавление постов, содержит в себе форму создания нового поста
@app.route('/add-post',methods = (['POST','GET']))
def add_post():
    # HTML форма для создания поста созданная при помощи библиотеки WTforms
    form = AddArticleForm(request.form)
    # Проверка на метод пост и на валидность введнных данных
    if request.method == 'POST' and form.validate():
        # Вытаскиваем данные из формы
        title = form.title.data
        description = form.description.data

        # Подключение к бд
        con = sqlite3.connect("blog.db")
        # Курсор
        cur = con.cursor()

        # Нам нужно текущее время для поля date нового поста 
        current_date = datetime.datetime.now()
        current_date = str(current_date.strftime('%Y-%m-%d %H:%M'))
        
        # Добавляем введенные данные в нашу таблицу
        cur.execute("INSERT INTO Posts(id,title,description,date) VALUES(?,?,?,?)", (None,title,description,current_date,))
        
        # Коммитим
        con.commit()
        # Закрываем соединение с бд
        con.close()
        
        # Редирект на главную страницу
        return redirect('/')
       
    return render_template('add-post.html',form = form)    


# Страница для редактирования постов, содержит в себе форму редактирования поста ссылка принимает параметр id который указывает на id нашего поста в таблице
@app.route('/edit-post/<string:id>',methods = (['POST','GET']))
def edit_post(id):    
    # Подключение к бд
    con = sqlite3.connect("blog.db")
    # Курсор
    cur = con.cursor()
    
    # Получаем все данные определенного поста
    cur.execute("SELECT * FROM Posts WHERE id = ?",(id,))

    # Один элемент
    post_to_edit = cur.fetchone()
    
    # Таже самая форма
    form = AddArticleForm(request.form)
    
    # В placeholder формы добавляем значения title and description
    form.title.data = post_to_edit[1]
    form.description.data = post_to_edit[2]
    
    # Закрываем соеденение
    con.close()
    
    # Проверка на метод пост и на валидность введнных данных
    if request.method == 'POST' and form.validate():
        
        # Получаем данные из формы для редактирования постов
        title = request.form['title']
        description = request.form['description']
        
        # Подключение к бд
        con = sqlite3.connect("blog.db")
        # Курсор
        cur = con.cursor()

        # Обновляем наш пост
        cur.execute("UPDATE Posts SET title = ?,description = ? WHERE id = ?",(title,description,id))
        
        # Коммитим
        con.commit()
        # Закрываем соединение с БД
        con.close()
        
        # Редирект на главную страницу
        return redirect('/')
       
    return render_template('edit-post.html',form = form)    

# Страница для удаления поста с определенным id,ссылка принимает параметр id который указывает на id нашего поста в таблице
@app.route('/delete-post/<string:id>', methods = (['POST','GET']))
def delete_post(id):
    # Подключение к бд
    con = sqlite3.connect("blog.db")
    # Курсор
    cur = con.cursor()

    # Удаляем пост при помощи кнопки на главной странице
    cur.execute("DELETE FROM Posts WHERE id = ?",(id,))

    # Коммитим
    con.commit()

    # Закрываем соединение
    con.close()

    # Вспоминаем про флеш 😥
    flash("You DELETE the post!",'danger')

    # Коментарии это круто!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return redirect('/')


@app.route('/post/<string:id>', methods = (['POST','GET']))
def post(id):
    
    # Подключение к бд
    con = sqlite3.connect("blog.db")
    # Курсор
    cur = con.cursor()

    # Удаляем пост при помощи кнопки на главной странице
    cur.execute("SELECT * FROM Posts WHERE id = ?",(id,))

    post = cur.fetchone()
    # Коммитим
    con.commit()

    # Закрываем соединение
    con.close()

    return render_template('post.html',post = post)    

if __name__ == '__main__':
    app.run(debug=True)
