#!/usr/bin/python3
"""quiz app"""


from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
import pymysql.cursors

app = Flask(__name__)

app.config['SECRET_KEY'] = '5e930833f20b0d4a5fa7505d70f5aa80'

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
    return render_template('main.html', title='Home')

@app.route('/main/posts')
def posts_page():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
    return render_template('posts.html', posts=posts, title='posts')

@app.route('/main/quiz')
def quiz_page():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
    return render_template('quiz.html', posts=posts, title='Quiz')


@app.route('/main/profile')
def profile_page():
    return render_template('profile.html', title='Profile')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    data = form.username.data
    if form.validate_on_submit():
        flash(f'Account created for {data}!')
        return redirect(url_for('about'))
    print("Form submission failed")
    return render_template('register.html', form=form, title='register')


@app.route('/login')
def Login_page():
    form = LoginForm()
    return render_template('login.html', form=form, title='Login')



if __name__ in '__main__':
    app.run(debug=True)
