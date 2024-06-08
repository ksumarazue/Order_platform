from flask import render_template, request, flash, redirect, url_for, Blueprint

from infra.users.user_repository import UserRepository

# from .infra.users.user_manager import UserManager

user_bp = Blueprint('user', __name__, url_prefix='/users') # czy /user może być users?

user_manager = UserRepository()

@user_bp.route('/')
def display_users():
    return render_template('users.html', users = user_manager.get_all_users())


@user_bp.route('/add', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_group = request.form['user_group']
        # try:
        user_manager.add_user(user_name, user_email, user_password, user_group)
            # user_manager.create_user(user_name, user_email, user_password, user_group)
            # flash("Successfully created expense", "success")
        return redirect(url_for('user.display_users'))
        # except InvalidExpenseError as err:
        #     flash(f"{err}", "danger")
    return render_template('add.html')