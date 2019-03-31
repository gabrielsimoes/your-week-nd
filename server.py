from users import *
from categories import events, categories
from flask import Flask, session, redirect, url_for, escape, request, render_template
from jinja2 import Environment, FileSystemLoader
import flask_login
import json
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = '109u2rn0c912nr0c91n0r190'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Flask-login user object
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if not user_exists(username):
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    password = request.form.get('password')

    if not user_exists(username):
        return

    user = User()
    user.id = username

    user.is_authenticated = check_user(username, password)

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# Routes for flask
@app.route('/', methods=['GET'])
def main():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for('login'))

    user_categories = get_categories(flask_login.current_user.id)

    print(user_categories)

    user_events = []
    for ev in events:
        print(ev['category'])
        if ev['category'] in user_categories:
            new_ev = ev.copy()
            new_ev['category'] = categories[ev['category']]
            user_events.append(new_ev)

    random.shuffle(user_events)

    return render_template('/landing.html', events=user_events, username=flask_login.current_user.id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    keys = [x for x in categories]
    tags = [categories[x] for x in categories]

    if request.method == 'GET':
        return render_template('/sign_up.html', endpoint='signup', tags=tags)

    username = request.form['username']
    password = request.form['password']

    selected_tags = []
    for opt in request.form:
        if opt != 'username' and opt != 'password':
            selected_tags.append(keys[int(opt)-1])

    if user_exists(username):
        return 'Bad signup'
    else:
        add_user(username, password, selected_tags)
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/sign_up.html', endpoint='login')

    username = request.form['username']
    password = request.form['password']

    if check_user(username, password):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('main'))

    return 'Bad login'

@app.route('/logout', methods=['POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))
