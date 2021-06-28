import sqlite3


connect = sqlite3.connect("blog.db")
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Posts(id integer primary key autoincrement, title varchar(100), description text, date text)")

connect.close()