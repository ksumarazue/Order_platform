from flask import render_template, request, flash, redirect, url_for, Blueprint
from infra.orders.order_manager import OrderRepository

order_bp = Blueprint('order', __name__, url_prefix='/orders') # czy /user może być users?

order_repository = OrderRepository()


@order_bp.route('/')
def display_orders():
    return render_template('orders.html', orders = order_repository.get_all_orders())


@order_bp.route('/add', methods=['GET', 'POST'])
def create_order():
    pass