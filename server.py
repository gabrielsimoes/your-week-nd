from users import *
from flask import Flask, session, redirect, url_for, escape, request
from jinja2 import Environment, FileSystemLoader
import flask_login
from template_engine import events

app = Flask(__name__)
app.secret_key = '109u2rn0c912nr0c91n0r190'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

templates = Environment(loader=FileSystemLoader('templates'))

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
    if flask_login.current_user.is_authenticated:
        return templates.get_template('landing.html').render(events=events)
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return '''
               <form action='/signup' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    password = request.form['password']

    if user_exists(username):
        return 'Bad signup'
    else:
        add_user(username, password)
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='/login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    password = request.form['password']

    if check_user(username, password):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('main'))

    return 'Bad login'

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'
