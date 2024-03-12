#!/usr/bin/python3
""" quiz models a"""


from datetime import datetime
from Aquiz import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    quiz = db.relationship('Quiz', backref='user', lazy=True)
    profile = db.relationship('Profile', backref='user', lazy=True, uselist=False)
    score = db.relationship('Score', backref='user', lazy=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    following = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follower', foreign_keys='Follower.followed_id', backref='followed', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"User('{self.username}', '{self.email})"
    
    def is_following(self, user):
        """Check if this user is following another user."""
        return db.session.query(Follower).filter(
            Follower.follower_id == self.id,
            Follower.followed_id == user.id
        ).count() > 0



class Profile (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Profile('{self.full_name}', '{self.avatar}, '{self.bio}')"


class Score (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.relationship('Question', backref='scores', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Score('{self.score}')"


class Quiz (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(100), nullable=False)
    quizpic = db.Column(db.String(255), nullable=False)
    questions = db.relationship('Question', backref='quiz_parent', lazy=True, cascade='all, delete-orphan')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Quiz('{self.title}', '{self.category}', '{self.level}', '{self.created_at}') "


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'))
    quiz = db.relationship('Quiz', backref=db.backref('childquestions', cascade='all, delete'))
    image_path = db.Column(db.String(255))  # Add field for image path/URL
    sound_path = db.Column(db.String(255))  # Add field for sound path/URL
    score = db.Column(db.Integer, default=10)
    options = db.relationship('Option', backref='question', lazy=True)

    def __repr__(self):
        return f"Question('{self.question_text}')"

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f"Option('{self.text}', '{self.is_correct}')"


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.relationship('User', backref='user_comments')
    def __repr__(self):
        return f"Comment('{self.text}', '{self.rating}', '{self.created_at}')"
