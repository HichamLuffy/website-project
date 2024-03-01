#!/usr/bin/python3
"""forms"""


import random
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from Aquiz.models import User
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange



class RegisterForm(FlaskForm):
    """register form"""
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
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
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('bio', validators=[DataRequired(), Length(min=0, max=150)])
    pfp = FileField('pfp', validators=[FileAllowed(['jpg', 'png'])])
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
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('category1', 'Questions'), ('category2', 'Sound'), ('category3', 'images')], validators=[DataRequired()])
    level = SelectField('Level', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], validators=[DataRequired()])
    questions = TextAreaField('Questions', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = SelectField('Correct Option', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], validators=[DataRequired()])
    num_questions = IntegerField('Number of Questions', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Create Quiz')
