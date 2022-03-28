from flask import Flask, abort
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello():
    return '<h1>Hello World</h1>'


@app.route('/about/')
def about():
    return '<h3>About Page</h3>'

@app.route('/capitalize/<word>')
def capitalize(word):
    return (f'<h1>Here is your capitalized word: {escape(word.upper())}</h1>')

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1,n2):
    return (f'<h1>{n1+n2}</h1>')

@app.route('/users/<int:user_id>')
def greet_user(user_id):
    users = ['Bob', 'Mary', 'Alex']
    try:
        return (f'<h1>{users[user_id]}</h1>')
    except IndexError:
        abort(404)

