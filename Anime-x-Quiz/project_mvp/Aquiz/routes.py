#!/usr/bin/python3
"""quiz routes"""


from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from Aquiz import app, db, bcrypt
from Aquiz.forms import RegisterForm, LoginForm
import pymysql.cursors
from Aquiz.models import User, Profile, Score, Quiz, Question, Option
from flask_login import login_user, current_user, logout_user, login_required



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
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegisterForm()
    data = form.username.data
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {data}! you can login', 'success')
        return redirect(url_for('Login_page'))
    print("Form submission failed")
    return render_template('register.html', form=form, title='register')


@app.route('/login', methods=['GET', 'POST'])
def Login_page():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    data = form.email.data
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberme.data)
            next_page = request.args.get('next')
            flash(f'login sucess', 'success')
            return redirect(next_page) if next_page else redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('about'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
