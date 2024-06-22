from flask import render_template, request, flash, redirect, url_for, Blueprint
from infra.orders.order_manager import OrderRepository

order_bp = Blueprint('order', __name__, url_prefix='/orders') # czy /user może być users?

order_repository = OrderRepository()


@order_bp.route('/')
def display_orders():
    return render_template('orders.html', orders = order_repository.get_all_orders())


@order_bp.route('/add', methods=['GET', 'POST'])
def create_order():
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
    return render_template('add_order.html')