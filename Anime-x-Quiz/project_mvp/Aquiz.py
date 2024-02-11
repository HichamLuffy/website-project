#!/usr/bin/python3
"""quiz app"""


from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'