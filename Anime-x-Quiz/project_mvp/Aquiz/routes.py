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
from datetime import datetime
from sqlalchemy import desc
from collections import defaultdict




connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin',
    database='AQZ',
    cursorclass=pymysql.cursors.DictCursor
)


def get_quiz_statistics(user_id):
    # Calculate total quiz attempts
    total_attempts = Score.query.filter_by(user_id=user_id).count()

    # Calculate average quiz score
    user_scores = Score.query.filter_by(user_id=user_id).all()
    total_score = sum(score.score for score in user_scores)
    average_score = total_score / max(len(user_scores), 1)
    average_score = round(average_score, 2)  # Round to 2 decimal places

    # Retrieve the most recent quiz played by the user
    most_recent_quiz = (
        db.session.query(Quiz.title)
        .join(Score, Score.quiz_id == Quiz.id)
        .filter(Score.user_id == user_id)
        .order_by(Score.id.desc())
        .first()
    )

    return {
        'total_attempts': total_attempts,
        'average_score': average_score,
        'most_recent_quiz': most_recent_quiz[0] if most_recent_quiz else None
    }

def get_profile_picture(user_id):
    user = User.query.get(user_id)
    if user and user.profile:
        return url_for('static', filename=f'images/{user.profile.avatar}')
    return 'default_avatar.jpg'


def get_total_score():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Retrieve the scores for the current user
        user_scores = Score.query.filter_by(user_id=current_user.id).all()

        # Calculate total score
        total_score = sum(score.score for score in user_scores)

        return total_score
    else:
        # Return 0 or handle the case when the user is not authenticated
        return 0  # You can adjust this based on your requirements


def get_leaderboard_data():
    leaderboard_data = {}
    # Query database to retrieve scores ordered by score in descending order
    scores = Score.query.order_by(Score.score.desc()).all()

    # Populate the leaderboard data with unique users and their total scores
    for score in scores:
        if score.user_id not in leaderboard_data:
            user = User.query.get(score.user_id)
            leaderboard_data[score.user_id] = (user.username, score.score)
        else:
            # Add the score to the existing user entry
            username, current_score = leaderboard_data[score.user_id]
            leaderboard_data[score.user_id] = (username, current_score + score.score)

    return leaderboard_data


def get_username(user_id):
    user = User.query.get(user_id)
    if user:
        return user.username
    return "Unknown User"


@app.route('/')
@app.route('/main')
def about():
    if current_user.is_authenticated:
        if 'static/' not in current_user.profile.avatar:
            image_file = url_for('static', filename='images/' + current_user.profile.avatar)
        else:
            image_file = '/' + current_user.profile.avatar
        total_score = get_total_score()
        return render_template('main.html', title='Home', total_score=total_score, image_file=image_file)
    return render_template('main.html', title='Home')

# @app.route('/main/posts')
# def posts_page():
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM posts')
#         posts = cursor.fetchall()
#     return render_template('posts.html', posts=posts, title='posts')


@app.route('/Quiz')
def quiz_page():
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    return render_template('quiz.html', title='Quiz', total_score=total_score, image_file=image_file)


@app.route('/main/profile')
def profile_page():
    image_file = current_user.profile.avatar
    total_score = get_total_score()
    return render_template('profile.html', title='Profile', image_file=image_file, total_score=total_score)

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
    total_score = get_total_score()
    return render_template('register.html', form=form, title='register', total_score=total_score)


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
    total_score = get_total_score()
    return render_template('login.html', form=form, title='Login', total_score=total_score)


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
    form_pfp.save(picture_path)  # Save the file
    img = Image.open(picture_path)  # Open the saved file
    img.thumbnail(resize_pic)
    img.save(picture_path)

    return (picture_fn)


@app.route('/main/account', methods=['GET', 'POST'])
@login_required
def account():
    form = updateprofileForm()
    if form.validate_on_submit():
        if form.new_avatar.data:
            print(form.new_avatar.data)
            current_user.profile.avatar = url_for('static', filename='images/' + form.new_avatar.data)
            print("im new avatar", current_user.profile.avatar)
        elif form.pfp.data:
            pic_file = save_pfp(form.pfp.data)
            current_user.profile.avatar = pic_file
            print(current_user.profile.avatar)
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
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    print(current_user.profile.avatar)
    print(image_file)
    quiz_stats = get_quiz_statistics(current_user.id)
    total_score = get_total_score()
    user = User.query.get_or_404(current_user.id)
    followers_count = user.followers.count()
    following_count = user.following.count()
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, total_score=total_score, total_attempts=quiz_stats['total_attempts'],
                            average_score=quiz_stats['average_score'],
                            most_recent_quiz=quiz_stats['most_recent_quiz'], followers_count=followers_count, following_count=following_count)


@app.route('/quiz')
@login_required
def quiz():
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    quizzes = Quiz.query.all()
    leaderboard_data = get_leaderboard_data()
    return render_template('quiz.html', title='Quiz', quizzes=quizzes, total_score=total_score, leaderboard_data=leaderboard_data, get_username=get_username, image_file=image_file)


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_questions(quiz_id):
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    num_questions = len(questions)
    if request.method == 'POST':
        total_questions = len(questions)
        user_score = 0  # Initialize user's score
        for question in questions:
            selected_option_id = int(request.form.get(f'question{question.id}'))
            print(f"Question {question.id} selected option ID: {selected_option_id}")
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
    return render_template('quiz_questions.html', title='Quiz Questions', quiz=quiz, questions=questions, total_score=total_score, num_questions=num_questions, image_file=image_file)


@app.route('/quiz/results')
@login_required
def quiz_results():
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    # Retrieve the latest score for the current user
    latest_score = Score.query.filter_by(user_id=current_user.id).order_by(desc(Score.id)).first()

    if latest_score:
        # Extract the score
        quiz_score = latest_score.score * 2
    else:
        quiz_score = 0

    return render_template('quiz_results.html', title='Quiz Results', quiz_score=quiz_score, total_score=total_score, image_file=image_file)


@app.route('/leaderboard')
def leaderboard():
    # Your view logic here
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    leaderboard_data = get_leaderboard_data()
    return render_template('quizleaderboard.html', title='Quiz', leaderboard_data=leaderboard_data, get_username=get_username, get_profile_picture=get_profile_picture, total_score=total_score, image_file=image_file)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':  # Check if the request is a POST request
        if current_user.is_authenticated:  # Check if the user is authenticated
            follow_user_id = request.form.get('user_id')
            if follow_user_id:  # Ensure a user ID is provided in the form data
                user_to_follow = User.query.get(follow_user_id)
                if user_to_follow and user_to_follow != current_user:
                    current_user.following.append(user_to_follow)
                    db.session.commit()
                    flash(f'You are now following {user_to_follow.username}', 'success')
                else:
                    flash('Invalid user ID or you cannot follow yourself', 'warning')
            else:
                flash('User ID not provided', 'danger')

    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    if 'static/' not in user.profile.avatar:
        user_image = url_for('static', filename='images/' + user.profile.avatar)
    else:
        user_image = '/' + user.profile.avatar
    print(user_image)
    quiz_stats = get_quiz_statistics(user_id)
    total_score = get_total_score()  # Or any other way to calculate total score for this user
    if (datetime.utcnow() - user.last_seen).total_seconds() < 300:  # 5 minutes threshold
        status = 'Online'
    else:
        status = 'Offline'
    followers_count = user.followers.count()
    following_count = user.following.count()
    return render_template('user_profile.html', title=user.username, user=user, user_image=user_image, total_score=total_score, image_file=image_file, total_attempts=quiz_stats['total_attempts'],
                            average_score=quiz_stats['average_score'],
                            most_recent_quiz=quiz_stats['most_recent_quiz'],
                            followers_count=followers_count, following_count=following_count, status=status)


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()