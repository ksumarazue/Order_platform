from flask import render_template, request, flash, redirect, url_for, Blueprint
from infra.product.product_manager import ProductRepository, InvalidProductError, NotFoundProductError

product_bp = Blueprint('product', __name__, url_prefix='/products')

product_repository = ProductRepository()


@product_bp.route('/')
def display_products():
    return render_template('products.html', products = product_repository.get_all_products())


@product_bp.route('/add', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_unit = request.form['product_unit']
        product_price = float(request.form['product_price'])
        product_ean = request.form['product_ean']
        print(product_name, product_unit, product_price, product_ean)
        try:
            product_repository.add_product(product_name, product_unit, product_price, product_ean)
            flash("Successfully created product", "success")
            return redirect(url_for('product.display_products'))
        except InvalidProductError as err:
            flash(f"{err}", "danger")
    return render_template('add_product.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if request.method == 'GET':
        print(product_id)
        try:
            product = product_repository.get_product_data(product_id)
            # print(product.prd_Name, product.prd_Unit, product.prd_PriceNet, product.prd_Ean)
            return render_template('edit_product.html', product=product)
        except NotFoundProductError as err:
            flash(f"{err}", 'danger')
            return redirect(url_for('product.display_products'))

    if request.method == 'POST':
        product_name = request.form['product_name']
        product_unit = request.form['product_unit']
        product_price = float(request.form['product_price'])
        product_ean = request.form['product_ean']
        try:
            product_repository.update_product(product_id, product_name, product_unit, product_price, product_ean)
            product_check = product_repository.get_product_data(product_id)
            print(product_check.prd_Id, product_check.prd_Name , product_check.prd_Unit ,product_check.prd_PriceNet, product_check.prd_Ean)
            return redirect(url_for('product.display_products'))
        except InvalidProductError as err:
            product = product_repository.get_product_data(product_id)
            return render_template('edit_product.html', product=product)


@product_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        product_repository.delete_product(product_id)
        flash('Succes delete product', 'success')
    except InvalidProductError as err:
        flash(f'{err}', 'danger')
    return redirect(url_for('product.display_products'))



