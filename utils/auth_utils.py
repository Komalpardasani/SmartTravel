import json
import bcrypt
import os

USER_DB_FILE = "data/users.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    return {}

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(email, password, name):
    users = load_users()
    if email in users:
        return False
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"name": name, "password": hashed_pw}
    save_users(users)
    return True

def authenticate_user(email, password):
    users = load_users()
    user = users.get(email)
    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return user["name"]
    return None



