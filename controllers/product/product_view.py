from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models.database import db
from models.product.product import Product
from models.user.user import User

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)


@product_blueprint.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


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

        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('product.products'))

    return render_template('add_product.html')


@product_blueprint.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']

        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.products'))

    return render_template('edit_product.html', product=product)


@product_blueprint.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if user.role not in ['admin', 'user']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.home'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('product.products'))
