#!/usr/bin/python3
"""quiz routes"""


import os
import secrets
import random
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from Aquiz import app, db, bcrypt
from Aquiz.forms import RegisterForm, LoginForm, updateprofileForm, New_QuizForm
import pymysql.cursors
from Aquiz.models import User, Profile, Score, Quiz, Question, Option
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify



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

# @app.route('/main/posts')
# def posts_page():
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM posts')
#         posts = cursor.fetchall()
#     return render_template('posts.html', posts=posts, title='posts')

@app.route('/Quiz')
def quiz_page():
    return render_template('quiz.html', title='Quiz')


@app.route('/main/profile')
def profile_page():
    image_file = current_user.profile.avatar
    return render_template('profile.html', title='Profile', image_file=image_file)

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
        default_avatar = random.choice(['astadefault.jpg', 'deathnotedefault.jpg', 'emmadefault.jpg', 'gojodefault.jpg', 'gokudefault.jpg',
                                        'kurabikadefault.jpg', 'levidefault.jpg', 'luffydefault.jpg', 'narutodefault.jpg', 'tanjirodefault.jpg', 'todorokidefault.jpg'])
        default_profile = Profile(full_name=form.username.data, avatar=f'static/images/{default_avatar}', bio='add bio.')
        user.profile = default_profile

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


def save_pfp(form_pfp):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pfp.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    print(picture_path)

    resize_pic = (256, 256)
    img = Image.open(form_pfp)
    img.thumbnail(resize_pic)
    img.save(picture_path)

    return (picture_fn)


@app.route('/main/account', methods=['GET', 'POST'])
@login_required
def account():
    form = updateprofileForm()
    if form.validate_on_submit():
        if form.new_avatar.data:
            current_user.profile.avatar = url_for('static', filename='images/' + form.new_avatar.data)
        elif form.pfp.data:
            pic_file = save_pfp(form.pfp.data)
            current_user.profile.avatar = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.profile.bio = form.bio.data
        db.session.commit()
        flash('you account has been updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.profile.bio
    image_file = current_user.profile.avatar
    print(image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route('/quiz')
def quiz():
    quizzes = Quiz.query.all()
    return render_template('quiz.html', title='Quiz', quizzes=quizzes)


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    if request.method == 'POST':
        total_questions = len(questions)
        user_score = 0  # Initialize user's score
        for question in questions:
            selected_option_id = int(request.form.get(f'question{question.id}'))
            selected_option = Option.query.get(selected_option_id)
            if selected_option.is_correct:
                user_score += 1  # Increment user's score for each correct answer

            # Save the user's answer and whether it's correct in the database
            score_entry = Score(
                user_answer=selected_option.text,
                is_correct=selected_option.is_correct,
                score=user_score,  # Update the user's score in the score entry
                question_id=question.id,
                quiz_id=quiz.id,
                user_id=current_user.id  # Assuming you have the current user available through Flask-Login
            )
            db.session.add(score_entry)
        
        # Commit changes to the database
        db.session.commit()

        flash('Answers submitted successfully', 'success')
        return redirect(url_for('quiz_results'))  # Redirect to a results page
    return render_template('quiz_questions.html', title='Quiz Questions', quiz=quiz, questions=questions)


@app.route('/quiz/results')
@login_required
def quiz_results():
    # Retrieve the scores for the current user and quiz
    user_scores = Score.query.filter_by(user_id=current_user.id).all()

    # Calculate total score
    total_score = sum(score.score for score in user_scores)

    # Get total number of questions for the quiz
    quiz_id = user_scores[0].quiz_id  # Assuming all scores are for the same quiz
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()

    # Count the number of correct answers
    correct_answers = sum(score.is_correct for score in user_scores)

    # Calculate percentage of correct answers
    percentage_correct = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    return render_template('quiz_results.html', title='Quiz Results', total_score=total_score, total_questions=total_questions, correct_answers=correct_answers, percentage_correct=percentage_correct)