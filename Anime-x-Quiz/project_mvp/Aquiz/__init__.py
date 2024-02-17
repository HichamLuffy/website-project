#!/usr/bin/python3
"""quiz app"""


from datetime import datetime
from flask import Flask
from Aquiz.forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5e930833f20b0d4a5fa7505d70f5aa80'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from Aquiz import routes