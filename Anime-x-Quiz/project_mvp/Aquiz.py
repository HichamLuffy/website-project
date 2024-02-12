#!/usr/bin/python3
"""quiz app"""


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def about():
    return render_template('main.html')


if __name__ in '__main__':
    app.run(debug=True)
