from flask import Blueprint, render_template, redirect, url_for, request, session, flash

from controllers.product.product_repository import ProductRepository
from models.database import db
from models.product.product import Product
from models.user.user import User

product_blueprint = Blueprint('product', __name__)

product_repository = ProductRepository()


@product_blueprint.route('/products')
def products():
    if 'user_id' not in session:
        flash('You need to be logged in to view this page.', 'danger')
        return redirect(url_for('user.login'))

    # all_products = Product.query.all()
    all_products = product_repository.get_all_products()
    if 'user_id' in session:
        user = User.query.get(session.get('user_id'))
    else:
        user = None
    return render_template('products.html', products=all_products, user=user)


@product_blueprint.route('/product/<int:product_id>')
def product_detail(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to view this page.', 'danger')
        return redirect(url_for('user.login'))

    product = product_repository.get_product_data(product_id)
    user = User.query.get(session.get('user_id')) if 'user_id' in session else None
    return render_template('product_detail.html', product=product, user=user)


@product_blueprint.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        product_repository.add_product(name, description, price)
        flash('Product added successfully.', 'success')
        return redirect(url_for('product.products'))

    return render_template('add_product.html', user=user)


@product_blueprint.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    product = product_repository.get_product_data(product_id)
    # product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        product_repository.update_product(product_id, name, description, price)
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.products'))

    return render_template('edit_product.html', product=product, user=user)


@product_blueprint.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    product_repository.delete_product(product_id)
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('product.products'))
