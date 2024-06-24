from flask import render_template, request, flash, redirect, url_for, Blueprint

from infra.users.user_repository import UserRepository, InvalidUserError, NotFoundUserError

# from .infra.users.user_manager import UserManager

user_bp = Blueprint('user', __name__, url_prefix='/users')

user_repository = UserRepository()


@user_bp.route('/')
def display_users():
    return render_template('users.html', users = user_repository.get_all_users())


@user_bp.route('/add', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_group = request.form['user_group']
        print(user_name, user_email, user_password, user_group)
        try:
            user_repository.add_user(user_name, user_email, user_password, user_group)
            flash("Successfully created expense", "success")
            return redirect(url_for('user.display_users'))
        except InvalidUserError as err:
            flash(f"{err}", "danger")
    return render_template('add_user.html')

@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def update_user_account(id):
    print(id)
    if request.method == 'GET':
        try:
            user = user_repository.get_user_data(id)
            return render_template('edit_user.html', user=user)
        except NotFoundUserError as err:
            flash(f"{err}", "danger")
            return redirect(url_for('user.display_users'))

    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_group = request.form['user_group']
        try:
            user_repository.update_user(id, user_name, user_email, user_password, user_group)
            return redirect(url_for('user.display_users'))
        except InvalidUserError as err:
            user = user_repository.get_user_data(id)
            return render_template('edit_user.html', user=user)

@user_bp.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        user_repository.delete_user(id)
        flash("Successfully deleted expense", "success")
    except InvalidUserError as err:
        flash(f'{err}', 'danger')
    return redirect(url_for('user.display_users'))