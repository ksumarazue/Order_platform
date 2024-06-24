from models.database import db
from models.product.product import Product


class ProductRepository:
    def get_all_products(self):
        return Product.query.all()

    def add_product(self, name, description, price):
        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()

    def update_product(self, product_id, name, description, price):
        product = self.get_product_data(product_id)
        if product:
            product.name = name
            product.description = description
            product.price = price
            db.session.commit()

    def delete_product(self, product_id):
        product = self.get_product_data(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()

    @staticmethod
    def get_product_data(product_id):
        return Product.query.get_or_404(product_id)