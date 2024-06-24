from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash

from controllers.user.user_repository import UserRepository
from models.user.user import User

user_blueprint = Blueprint('user', __name__)

user_repository = UserRepository()

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('user.home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('user.home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@user_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        flash('You need to be logged in as admin to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        user_id = request.form.get('user_id')

        if action == 'create':
            user_repository.create_user(username, password, role)
            flash(f'User {username} created successfully.', 'success')
        elif action == 'update':
            user_repository.update_user(user_id, username, password, role)
            flash(f'User updated successfully.', 'success')
        elif action == 'delete':
            user_repository.delete_user(user_id)
            flash(f'User deleted successfully.', 'success')
    return render_template('admin.html', users=user_repository.get_all_users(), user=user)

@user_blueprint.route('/home')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user, admin=user.role == 'admin', client=user.role == 'client')
    else:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('user.login'))

@user_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('user.login'))
