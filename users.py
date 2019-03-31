import pickle
import bcrypt

def load_users():
    try:
        users_file = open("users.pickle", "rb")
        return pickle.load(users_file)
    except FileNotFoundError:
        return {}
        pass

def save_users(users_db):
    with open("users.pickle", "wb") as out_file:
        pickle.dump(users_db, out_file, pickle.HIGHEST_PROTOCOL)

def user_exists(username):
    users_db = load_users()
    if username in users_db:
        return True
    else:
        return False

def add_user(username, password, categories):
    users_db = load_users()
    if not user_exists(username):
        users_db[username] = {
            'pass': bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
            'categories': categories,
        }
        save_users(users_db)

def check_user(username, password):
    users_db = load_users()
    if not user_exists(username):
        return False
    else:
        return bcrypt.checkpw(password.encode('utf8'), users_db[username]['pass'])

def get_categories(username):
    users_db = load_users()
    if not user_exists(username):
        return []
    else:
        return users_db[username]['categories']

