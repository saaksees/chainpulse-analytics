from flask_login import UserMixin
from flask_bcrypt import (generate_password_hash, check_password_hash)
from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user
from datetime import datetime
import json, os

USERS_FILE = 'config/users.json'

# ── User Model ──────────────────────
class User(UserMixin):
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password_hash = data['password_hash']
        self.role = data['role']
        self.email = data.get('email', '')
        self.full_name = data.get('full_name', '')
        self.created_at = data.get('created_at', '')
        self.last_login = data.get('last_login', 'Never')
        self.uploads_count = data.get('uploads_count', 0)
        self.initials = (data.get('full_name') or data.get('username', 'U'))[:2].upper()

# ── Storage ──────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return _create_defaults()
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(data):
    os.makedirs('config', exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _create_defaults():
    data = {
        "users": [
            {
                "id": "1",
                "username": "admin",
                "password_hash": generate_password_hash("chainpulse123").decode('utf-8'),
                "role": "admin",
                "email": "admin@chainpulse.com",
                "full_name": "Administrator",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "last_login": "Never",
                "uploads_count": 0
            },
            {
                "id": "2",
                "username": "analyst",
                "password_hash": generate_password_hash("analyst123").decode('utf-8'),
                "role": "analyst",
                "email": "analyst@chainpulse.com",
                "full_name": "Data Analyst",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "last_login": "Never",
                "uploads_count": 0
            },
            {
                "id": "3",
                "username": "viewer",
                "password_hash": generate_password_hash("viewer123").decode('utf-8'),
                "role": "viewer",
                "email": "viewer@chainpulse.com",
                "full_name": "Report Viewer",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "last_login": "Never",
                "uploads_count": 0
            }
        ]
    }
    save_users(data)
    return data

# ── User lookups ─────────────────────
def get_user_by_id(user_id):
    for u in load_users()['users']:
        if str(u['id']) == str(user_id):
            return User(u)
    return None

def get_user_by_username(username):
    for u in load_users()['users']:
        if u['username'] == username:
            return User(u)
    return None

def get_all_users():
    return [User(u) for u in load_users()['users']]

# ── Auth operations ──────────────────
def verify_password(username, password):
    for u in load_users()['users']:
        if u['username'] == username:
            return check_password_hash(u['password_hash'], password)
    return False

def update_last_login(username):
    data = load_users()
    for u in data['users']:
        if u['username'] == username:
            u['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_users(data)

def create_user(username, password, role, email, full_name):
    data = load_users()
    for u in data['users']:
        if u['username'] == username:
            return False, "Username already taken"
    
    max_id = max([int(u['id']) for u in data['users']], default=0)
    data['users'].append({
        "id": str(max_id + 1),
        "username": username,
        "password_hash": generate_password_hash(password).decode('utf-8'),
        "role": role,
        "email": email,
        "full_name": full_name,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "last_login": "Never",
        "uploads_count": 0
    })
    save_users(data)
    return True, "User created"

def update_profile(user_id, full_name, email):
    data = load_users()
    for u in data['users']:
        if str(u['id']) == str(user_id):
            u['full_name'] = full_name
            u['email'] = email
    save_users(data)
    return True, "Profile updated"

def change_password(user_id, old_pass, new_pass):
    data = load_users()
    for u in data['users']:
        if str(u['id']) == str(user_id):
            if check_password_hash(u['password_hash'], old_pass):
                u['password_hash'] = generate_password_hash(new_pass).decode('utf-8')
                save_users(data)
                return True, "Password changed"
            return False, "Wrong current password"
    return False, "User not found"

def delete_user(user_id):
    data = load_users()
    data['users'] = [u for u in data['users'] if str(u['id']) != str(user_id)]
    save_users(data)

def update_user_role(user_id, new_role):
    data = load_users()
    for u in data['users']:
        if str(u['id']) == str(user_id):
            u['role'] = new_role
    save_users(data)

# ── Decorators ───────────────────────
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator