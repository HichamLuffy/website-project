#!/usr/bin/python3
"""quiz app"""


from flask import Flask, render_template
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(
    host='localhost',
    user='Luffy',
    password='hhh123',
    database='AQZ',
    cursorclass=pymysql.cursors.DictCursor
)
@app.route('/')
@app.route('/main')
def about():
    return render_template('main.html')

@app.route('/main/posts')
def posts_page():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
    return render_template('posts.html', posts=posts)

if __name__ in '__main__':
    app.run(debug=True)
