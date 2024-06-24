from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from infra.users.user import User

auth_bp = Blueprint('login', __name__, url_prefix='/login')

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     user = User.query.filter_by(username=username).first()
    #     if user and password:
    #         login_user(user)
    #         return redirect(url_for('auth.home'))
    #     else:
    #         flash('Login unsuccessful. Please check your credentials.', 'danger')
    # return render_template('login.html')


# @auth_bp.route('/logout')
# # @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


# @auth_bp.route('/home')
# # @login_required
# def home():
#     return render_template('home.html')