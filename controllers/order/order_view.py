from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models.database import db
from models.order.order import Order, OrderItem
from models.product.product import Product
from models.user.user import User

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('You need to be logged in to view the cart.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'client':
        flash('Only clients can view the cart.', 'danger')
        return redirect(url_for('user.home'))

    cart_items = session.get('cart', [])
    products = Product.query.filter(Product.id.in_([item['product_id'] for item in cart_items])).all()
    total = sum(
        item['quantity'] * next((p.price for p in products if p.id == item['product_id']), 0) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, products=products, total=total)


@order_blueprint.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to add items to the cart.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'client':
        flash('Only clients can add items to the cart.', 'danger')
        return redirect(url_for('user.home'))

    quantity = int(request.form['quantity'])
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        cart.append({'product_id': product_id, 'quantity': quantity})
    session['cart'] = cart
    flash('Item added to cart.', 'success')
    return redirect(url_for('product.products'))


@order_blueprint.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to update the cart.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'client':
        flash('Only clients can update the cart.', 'danger')
        return redirect(url_for('user.home'))

    quantity = int(request.form['quantity'])
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] = quantity
            break
    session['cart'] = cart
    flash('Cart updated.', 'success')
    return redirect(url_for('order.cart'))


@order_blueprint.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to remove items from the cart.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'client':
        flash('Only clients can remove items from the cart.', 'danger')
        return redirect(url_for('user.home'))

    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart
    flash('Item removed from cart.', 'success')
    return redirect(url_for('order.cart'))


@order_blueprint.route('/cart/confirm', methods=['POST'])
def confirm_cart():
    if 'user_id' not in session:
        flash('You need to be logged in to confirm the cart.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role != 'client':
        flash('Only clients can confirm the cart.', 'danger')
        return redirect(url_for('user.home'))

    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty.', 'danger')
        return redirect(url_for('order.cart'))

    order = Order(user_id=user.id, status='confirmed')
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        db.session.add(order_item)

    db.session.commit()
    session.pop('cart', None)
    flash(f'Order #{order.id} confirmed successfully.', 'success')
    return redirect(url_for('order.orders'))


@order_blueprint.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('You need to be logged in to view orders.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role == 'client':
        orders = Order.query.filter_by(user_id=user.id).all()
    else:
        orders = Order.query.all()

    orders_with_users = []
    for order in orders:
        order_user = User.query.get(order.user_id)
        orders_with_users.append((order, order_user))

    return render_template('orders.html', orders_with_users=orders_with_users, user=user)


@order_blueprint.route('/order/<int:order_id>')
def order_detail(order_id):
    if 'user_id' not in session:
        flash('You need to be logged in to view the order.', 'danger')
        return redirect(url_for('user.login'))

    order = Order.query.get_or_404(order_id)
    user = User.query.get(session['user_id'])
    order_user = User.query.get(order.user_id)

    if user.role == 'client' and order.user_id != user.id:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('order.orders'))

    return render_template('order_detail.html', order=order, user=user, order_user=order_user)


@order_blueprint.route('/order/<int:order_id>/update_status', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session:
        flash('You need to be logged in to update the order.', 'danger')
        return redirect(url_for('user.login'))

    order = Order.query.get_or_404(order_id)
    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to update this order.', 'danger')
        return redirect(url_for('order.orders'))

    new_status = request.form['status']
    order.status = new_status
    db.session.commit()
    flash('Order status updated successfully.', 'success')
    return redirect(url_for('order.order_detail', order_id=order_id))
