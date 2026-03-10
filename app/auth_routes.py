from flask import (Blueprint, render_template, request, redirect, url_for, flash, jsonify, session)
from flask_login import (login_user, logout_user, current_user)
from app.auth import *

auth = Blueprint('auth', __name__)

# ── Login ────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if verify_password(email, password):
            user = get_user_by_email(email)
            login_user(user, remember=True)
            update_last_login(email)
            return redirect(url_for('main.home'))
        else:
            error = "Invalid email or password"
    
    return render_template('login.html', error=error)

# ── Logout ───────────────────────────
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/force-logout')
def force_logout():
    """Force logout and clear all sessions"""
    from flask import session
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

# ── My Profile ───────────────────────
@auth.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=current_user)

# ── Update profile ───────────────────
@auth.route('/api/profile/update', methods=['POST'])
def update_profile_api():
    if not current_user.is_authenticated:
        return jsonify({'success': False}), 401
    
    data = request.get_json()
    ok, msg = update_profile(current_user.id,
                           data.get('full_name', ''),
                           data.get('email', ''))
    return jsonify({'success': ok, 'message': msg})

# ── Change password ──────────────────
@auth.route('/api/profile/password', methods=['POST'])
def change_password_api():
    if not current_user.is_authenticated:
        return jsonify({'success': False}), 401
    
    data = request.get_json()
    ok, msg = change_password(current_user.id,
                            data.get('old_password', ''),
                            data.get('new_password', ''))
    return jsonify({'success': ok, 'message': msg})

# ── Admin: list users ─────────────────
@auth.route('/admin/users')
@require_role('admin')
def admin_users():
    users = get_all_users()
    return render_template('admin_users.html', users=users)

# ── Admin: create user ────────────────
@auth.route('/api/admin/users/create', methods=['POST'])
@require_role('admin')
def admin_create_user():
    data = request.get_json()
    ok, msg = create_user(data.get('username', ''),
                         data.get('password', ''),
                         data.get('role', 'viewer'),
                         data.get('email', ''),
                         data.get('full_name', ''))
    return jsonify({'success': ok, 'message': msg})

# ── Admin: delete user ────────────────
@auth.route('/api/admin/users/delete/<uid>', methods=['POST'])
@require_role('admin')
def admin_delete_user(uid):
    if str(uid) == str(current_user.id):
        return jsonify({'success': False,
                       'message': "Can't delete yourself"})
    
    delete_user(uid)
    return jsonify({'success': True,
                   'message': 'User deleted'})

# ── Admin: change role ────────────────
@auth.route('/api/admin/users/role/<uid>', methods=['POST'])
@require_role('admin')
def admin_change_role(uid):
    if str(uid) == str(current_user.id):
        return jsonify({'success': False,
                       'message': "Can't change own role"})
    
    data = request.get_json()
    update_user_role(uid, data.get('role'))
    return jsonify({'success': True,
                   'message': 'Role updated'})

# ── 403 handler ──────────────────────
@auth.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403