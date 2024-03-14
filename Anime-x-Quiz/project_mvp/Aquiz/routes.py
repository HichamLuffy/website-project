#!/usr/bin/python3
"""quiz routes"""


import os
import secrets
import random
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from Aquiz import app, db, bcrypt
from Aquiz.forms import RegisterForm, LoginForm, updateprofileForm, New_QuizForm
import pymysql.cursors
from Aquiz.models import User, Profile, Score, Quiz, Question, Option, Follower, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint, jsonify
from datetime import datetime
from sqlalchemy import desc
from collections import defaultdict


bp = Blueprint('main', __name__)


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
    if user and user.profile and user.profile.avatar:
        # Check if the avatar attribute already contains the 'static/' part
        if user.profile.avatar.startswith('static/'):
            # Strip 'static/' and then create the correct URL
            return url_for('static', filename=user.profile.avatar[len('static/'):])
        else:
            # If 'static/' is not part of the avatar attribute, create the URL directly
            return url_for('static', filename='images/' + user.profile.avatar)
    else:
        # Return the URL for the default avatar
        return url_for('static', filename='images/default_avatar.jpg')


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
    # Query database to retrieve users with their total scores, ordered by score in descending order
    users_scores = db.session.query(
        User.id,
        User.username,
        db.func.sum(Score.score).label('total_score')
    ).join(Score, User.id == Score.user_id
    ).group_by(User.id, User.username
    ).order_by(db.desc('total_score')
    ).all()

    # Create a list of tuples (user_id, username, total_score)
    leaderboard_list = [(user_id, username, total_score) for user_id, username, total_score in users_scores]

    return leaderboard_list


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


def save_pfp(form_pfp, resize_dimensions=(300, 300)):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pfp.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    print(picture_path)

    form_pfp.save(picture_path)  # Save the file
    img = Image.open(picture_path)  # Open the saved file
    img.thumbnail(resize_dimensions)
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
    # quizzes = Quiz.query.all()
    quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
    print('hello i aam', current_user.id)
    print('hello we are ', quizzes)
    quizzes_with_images = []
    image_path = []
    if quizzes:
        print('hello again ', quizzes)
        for quiz in quizzes:  # Exclude the last quiz
            print('i am ', quiz)
            image_path = url_for('static', filename='images/quizzes/' + quiz.quizpic) if quiz.quizpic else None
            quizzes_with_images.append((quiz, image_path))
    template_context = {
    'title': 'Account',
    'image_file': image_file,
    'form': form,
    'total_score': total_score,
    'total_attempts': quiz_stats['total_attempts'],
    'average_score': quiz_stats['average_score'],
    'most_recent_quiz': quiz_stats['most_recent_quiz'],
    'followers_count': followers_count,
    'following_count': following_count,
    }
    if quizzes_with_images:
        template_context['quizzes_with_images'] = quizzes_with_images
        print('hehehe')

    if image_path:
        template_context['image_path'] = image_path
    return render_template('account.html', **template_context)


@app.route('/quiz')
@login_required
def quiz():
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    total_score = get_total_score()
    quizzes = Quiz.query.all()
    quizzes.reverse()
    leaderboard_data = get_leaderboard_data()

    # Prepare quizzes with image paths
    quizzes_with_images = []
    for quiz in quizzes[:-1]:  # Exclude the last quiz
        image_path = url_for('static', filename='images/quizzes/' + quiz.quizpic) if quiz.quizpic else None
        quizzes_with_images.append((quiz, image_path))

    # Handle the last quiz separately if needed
    quizzes = Quiz.query.all()
    if quizzes:
        last_quiz_image_path = url_for('static', filename='images/quizzes/' + quizzes[-1].quizpic)
    else:
        last_quiz_image_path = None

    return render_template('quiz.html', title='Quiz',quizzes=quizzes , quizzes_with_images=quizzes_with_images, total_score=total_score, leaderboard_data=leaderboard_data, get_username=get_username, image_file=image_file, last_quiz_image_path=last_quiz_image_path)


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
        user_score = 0  # Initialize user's score
        response_times = request.form.getlist('response_time')
        for idx, question in enumerate(questions):
            selected_option_id_str = request.form.get(f'question{question.id}')
            response_time = float(response_times[idx]) if idx < len(response_times) else 0  # Safe retrieval and conversion
            if selected_option_id_str:
                selected_option_id = int(selected_option_id_str)
                selected_option = Option.query.get(selected_option_id)
                question_score = 0  # Initialize score for this question
                
                # Calculate score based on correctness and response time
                if selected_option and selected_option.is_correct:
                    base_score = 10  # Correct answer score
                    speed_bonus = max(0, 5 - (5 * max(0, response_time - 10) / 10))  # Calculate speed bonus
                    question_score = base_score + speed_bonus
                    user_score += question_score

                # Save the user's answer and whether it's correct in the database along with score
                score_entry = Score(
                    user_answer=selected_option.text if selected_option else '',
                    is_correct=selected_option.is_correct if selected_option else False,
                    score=question_score,
                    question_id=question.id,
                    quiz_id=quiz.id,
                    user_id=current_user.id
                )
                db.session.add(score_entry)
        
        db.session.commit()
        flash('Answers submitted successfully', 'success')
        return redirect(url_for('quiz_results', quiz_id=quiz_id))
    return render_template('quiz_questions.html', title='Quiz Questions', quiz=quiz, questions=questions, total_score=total_score, num_questions=num_questions, image_file=image_file)


@app.route('/quiz/results/<int:quiz_id>')
@login_required
def quiz_results(quiz_id):
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar

    # Fetch the timestamp of the latest attempt for the current user and quiz
    latest_attempt_time = db.session.query(db.func.max(Score.created_at)).filter_by(quiz_id=quiz_id, user_id=current_user.id).scalar()

    # Assuming you want to fetch scores only for this latest attempt,
    # we filter scores not just by quiz_id and user_id but also by this latest timestamp
    scores = Score.query.filter_by(quiz_id=quiz_id, user_id=current_user.id).filter(Score.created_at == latest_attempt_time).all()

    # Calculate total score and prepare details for each question
    total_score = sum(score.score for score in scores)
    details = []
    for score in scores:
        question = Question.query.get(score.question_id)
        # Assuming user_answer stores option ID correctly as a string that can be converted to integer
        option_id = int(score.user_answer) if score.user_answer.isdigit() else None
        option = Option.query.get(option_id) if option_id else None
        detail = {
            'question_text': question.question_text,
            'selected_option_text': option.text if option else "N/A",
            'is_correct': score.is_correct,
            'score_awarded': score.score
        }
        details.append(detail)

    return render_template('quiz_results.html', title='Quiz Results', total_score=total_score, details=details, image_file=image_file)


@app.route('/leaderboard')
def leaderboard():
    # Your view logic here
    total_score = get_total_score()
    leaderboard_data = get_leaderboard_data()
    if current_user.is_authenticated:
        if 'static/' not in current_user.profile.avatar:
            image_file = url_for('static', filename='images/' + current_user.profile.avatar)
        else:
            image_file = '/' + current_user.profile.avatar
        return render_template('quizleaderboard.html', title='Quiz', leaderboard_data=leaderboard_data, get_username=get_username, get_profile_picture=get_profile_picture, total_score=total_score, image_file=image_file)
    return render_template('quizleaderboard.html', title='Quiz', leaderboard_data=leaderboard_data, get_username=get_username, get_profile_picture=get_profile_picture, total_score=total_score)


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
    if current_user.is_authenticated:
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
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    quizzes.reverse()
    quizzes_with_images = []
    image_path = []
    if quizzes:
        for quiz in quizzes:  # Exclude the last quiz
            image_path = url_for('static', filename='images/quizzes/' + quiz.quizpic) if quiz.quizpic else None
            quizzes_with_images.append((quiz, image_path))
    
    template_context = {
    'title': user.username,
    'user': user,
    'user_image': user_image,
    'total_score': total_score,
    'total_attempts': quiz_stats['total_attempts'],
    'average_score': quiz_stats['average_score'],
    'most_recent_quiz': quiz_stats['most_recent_quiz'],
    'followers_count': followers_count,
    'following_count': following_count,
    'status': status
    }

    if current_user.is_authenticated:
        template_context['image_file'] = image_file
        
    if quizzes_with_images:
        template_context['quizzes_with_images'] = quizzes_with_images

    if image_path:
        template_context['image_path'] = image_path

    return render_template('user_profile.html', **template_context)


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def quiz_pfp(form_pfp, resize_width=800):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pfp.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/quizzes', picture_fn)
    print(picture_path)

    form_pfp.save(picture_path)  # Save the file
    img = Image.open(picture_path)  # Open the saved file
    
    # Calculate new height maintaining aspect ratio
    aspect_ratio = img.height / img.width
    new_height = int(resize_width * aspect_ratio)
    
    img = img.resize((resize_width, new_height))
    
    img.save(picture_path)

    return picture_fn


@app.route('/Create_Quiz', methods=['GET', 'POST'])
@login_required
def Create_Quiz():
    if 'static/' not in current_user.profile.avatar:
        image_file = url_for('static', filename='images/' + current_user.profile.avatar)
    else:
        image_file = '/' + current_user.profile.avatar
    form = New_QuizForm()
    if form.validate_on_submit():
        # check if the post request has the file part
        if form.quizpic.data:
            quizpfp = quiz_pfp(form.quizpic.data, resize_width=800)
            print(quizpfp)
        
        # Create and add the new quiz
        new_quiz = Quiz(
            title=form.title.data,
            category=form.category.data,
            level=form.level.data,
            quizpic=quizpfp,  # Assuming you handle file saving elsewhere
            user_id=current_user.id
        )
        print(quizpfp)
        db.session.add(new_quiz)
        try:
            db.session.commit() # Commit here to obtain an ID for the quiz
        except Exception as e:
            print(f"Error committing to database: {e}")
            db.session.rollback()   

        # Process dynamically added questions and options
        num_questions = int(form.num_questions.data)
        for i in range(1, num_questions + 1):
            question_text = request.form.get(f'question{i}', None)
            if question_text:  # Only proceed if question_text is not None
                new_question = Question(question_text=question_text, quiz_id=new_quiz.id)
                db.session.add(new_question)
                db.session.flush()
                for j in range(1, 5):  # Assuming 4 options per question
                    option_text = request.form.get(f'option{i}_{j}')
                    is_correct = request.form.get(f'correct_option{i}') == str(j)
                    if option_text:  # Ensure option text is not empty
                        new_option = Option(text=option_text, is_correct=is_correct, question_id=new_question.id)
                        db.session.add(new_option)
            try:
                db.session.commit() # Commit here to obtain an ID for the question
            except Exception as e:
                print(f"Error committing to database: {e}")
                db.session.rollback() 
        
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('quiz'))  # Redirect as appropriate
    else:
        print(form.errors)
        flash('error something happened', 'danger')

    return render_template('create_quiz.html', title='Create New Quiz', form=form, image_file=image_file)


@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id == current_user.id:
        # Manually delete related questions and their options
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        for question in questions:
            Option.query.filter_by(question_id=question.id).delete()
            db.session.delete(question)
        
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully.', 'success')
    else:
        flash('You do not have permission to delete this quiz.', 'danger')
    return redirect(url_for('account'))


@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('user_profile', user_id=user.id))
    
    # Check if already following
    if current_user.is_following(user):
        flash('You are already following this user.', 'info')
        return redirect(url_for('user_profile', user_id=user.id))
    
    # Follow the user
    new_follow = Follower(follower_id=current_user.id, followed_id=user.id)
    db.session.add(new_follow)
    db.session.commit()
    flash('You are now following {}.'.format(user.username), 'success')
    return redirect(url_for('user_profile', user_id=user.id))

# You might need to add an is_following method to your User model
def is_following(self, user):
    return self.following.filter_by(followed_id=user.id).count() > 0


@app.route('/user/followers/<int:user_id>')
def user_followers(user_id):
    user = User.query.get_or_404(user_id)
    # Assuming 'followers' is a relationship attribute that returns instances of a relationship model,
    # and each instance has a 'follower' attribute pointing to the User who is following 'user'
    followers = user.followers
    followers_list = [{'username': follower.follower.username, 'id': follower.follower.id} for follower in followers]
    return jsonify(followers_list)

@app.route('/user/following/<int:user_id>')
def user_following(user_id):
    user = User.query.get_or_404(user_id)
    # Assuming 'following' returns a list of relationships where 'user' is the follower
    following = user.following
    following_list = [{'username': followed.followed.username, 'id': followed.followed.id} for followed in following]
    return jsonify(following_list)


@app.route('/search_quizzes_ajax')
def search_quizzes_ajax():
    search_term = request.args.get('search', '')
    if search_term:
        # Search for quizzes by title
        matching_quizzes = Quiz.query.filter(Quiz.title.ilike(f'%{search_term}%')).all()

        # Prepare the data for JSON response
        quizzes_data = [{'id': quiz.id, 'title': quiz.title, 'image_path': url_for('static', filename='images/quizzes/' + quiz.quizpic)} for quiz in matching_quizzes]
    else:
        quizzes_data = []

    return jsonify(quizzes_data)


@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    comments.reverse()
    comments_data = [{'username': comment.author.username, 
                    'profile_pic': url_for('static', filename='images/' + comment.author.profile.avatar) if 'static/' not in comment.author.profile.avatar else '/' + comment.author.profile.avatar, 
                    'rating': comment.rating, 
                    'text': comment.text} 
                    for comment in comments]
    return jsonify(comments_data)


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    comment_text = data.get('text')
    comment_rating = data.get('rating')
    # You may need to authenticate the user and get the user_id before adding the comment
    if not current_user.is_authenticated:
        return jsonify({'error': 'User must be logged in to add a comment'}), 401

    # Create a new Comment object
    new_comment = Comment(user_id=current_user.id, text=comment_text, rating=comment_rating)

    # Add the new comment to the database
    db.session.add(new_comment)
    db.session.commit()
    if 'static/' not in new_comment.author.profile.avatar:
        image_file = url_for('static', filename='images/' + new_comment.author.profile.avatar)
    else:
        image_file = '/' + new_comment.author.profile.avatar
    if 'static/' not in new_comment.author.profile.avatar:
        user_image = url_for('static', filename='images/' + new_comment.author.profile.avatar)
    else:
        user_image = '/' + new_comment.author.profile.avatar
    # Return the newly added comment as JSON response
    comment_data = {'username': new_comment.author.username, 'profile_pic': user_image, 'rating': new_comment.rating, 'text': comment_text}
    return jsonify(comment_data), 201