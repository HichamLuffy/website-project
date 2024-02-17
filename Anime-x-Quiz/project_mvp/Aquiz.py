#!/usr/bin/python3
"""quiz app"""


from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
from models import User, Profile, Score, Quiz, Question, option

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e930833f20b0d4a5fa7505d70f5aa80'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin',
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
        flash(f'Account created for {data}!', 'success')
        return redirect(url_for('about'))
    print("Form submission failed")
    return render_template('register.html', form=form, title='register')


@app.route('/login', methods=['GET', 'POST'])
def Login_page():
    form = LoginForm()
    data = form.email.data
    if form.validate_on_submit():
        if form.email.data == 'luffy@gmail.com' and form.password.data == 'hhh123':
            flash(f'login sucess', 'success')
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login')



if __name__ in '__main__':
    app.run(debug=True)
