#!/usr/bin/python3
"""forms"""


import random
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from Aquiz.models import User, Quiz
from better_profanity import profanity
from flask_login import current_user
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange



def validate_no_profanity(form, field):
    if profanity.contains_profanity(field.data):
        raise ValidationError('Please avoid using profane language')


class RegisterForm(FlaskForm):
    """register form"""
    username = StringField('username', validators=[DataRequired(), validate_no_profanity, Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = password = PasswordField('Confirm password',
                                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """register form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=25)])
    rememberme = BooleanField('Remember me')
    submit = SubmitField('Login')

class updateprofileForm(FlaskForm):
    """register form"""
    username = StringField('username', validators=[DataRequired(), validate_no_profanity, Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('bio', validators=[DataRequired(), validate_no_profanity, Length(min=0, max=150)])
    pfp = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    default_avatar = [
        ('', ''),
        ('astadefault.jpg', 'Asta'),
        ('deathnotedefault.jpg', 'Death Note'),
        ('emmadefault.jpg', 'Emma'),
        ('gojodefault.jpg', 'Gojo'),
        ('gokudefault.jpg', 'Goku'),
        ('kurabikadefault.jpg', 'Kurabi'),
        ('levidefault.jpg', 'Levi'),
        ('luffydefault.jpg', 'Luffy'),
        ('narutodefault.jpg', 'Naruto'),
        ('tanjirodefault.jpg', 'Tanjiro'),
        ('todorokidefault.jpg', 'Todoroki')
    ]
    new_avatar = SelectField('Select New Avatar', choices=default_avatar)

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class New_QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), validate_no_profanity, Length(min=5, max=40)], render_kw={"class": "form-input"})
    category = SelectField('Category', choices=[('category0', ''), ('Questions', 'Questions'), ('Sound', 'Sound'), ('Images', 'Images')], validators=[DataRequired()], render_kw={"class": "form-select"})
    level = SelectField('Level', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], validators=[DataRequired()], render_kw={"class": "form-select"})
    quizpic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])], render_kw={"class": "form-file"})
    num_questions = IntegerField('Number of Questions', validators=[DataRequired(), NumberRange(min=1, max=10)], render_kw={"class": "form-input"})
    submit = SubmitField('Create Quiz', render_kw={"id": "submit_quiz"})

    def validate_title(self, title):
        quiz = Quiz.query.filter_by(title=title.data).first()
        if quiz:
            flash('This Quiz Already Exists. Please choose a different one.', 'danger')
            raise ValidationError('This Quiz Already Exists. Please choose a different one.')

    def validate_questions(self, questions):
        # Split questions by newline character
        question_list = questions.data.split('\n')
        
        # Remove any empty strings from the list
        question_list = [question.strip() for question in question_list if question.strip()]

        # Check if there are any duplicate questions
        if len(question_list) != len(set(question_list)):
            raise ValidationError('Questions must be unique.')
