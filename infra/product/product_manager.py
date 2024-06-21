from ..database import db
from ..product.product import Product


class InvalidProductError(Exception):
    pass


class NotFoundProductError(Exception):
    pass


class ProductRepository:
    def get_all_products(self):
        return Product.query.all()

    def add_product(self, product_name: str, product_unit: str, product_price: float, product_ean: int):    #zmienić product_ean na opcjonalny
        if not product_name or not product_unit or not product_price:
            raise InvalidProductError("Invalid product data")
        new_product = Product(prd_Name=product_name, prd_Unit=product_unit, prd_PriceNet=product_price, prd_Ean=product_ean)
        db.session.add(new_product)
        db.session.commit()

    def update_product(self, product_id, prd_Name, prd_Unit, prd_PriceNet, prd_Ean):
        product = self.get_product_data(product_id)
        if not prd_Name or not prd_Unit or not prd_PriceNet:
            raise InvalidProductError("Invalid product data")
        if product:
            product.prd_Name = prd_Name
            product.prd_Unit = prd_Unit
            product.prd_PriceNet = prd_PriceNet
            product.prd_Ean = prd_Ean
            db.session.commit()


    def delete_product(self, product_id):
        product = self.get_product_data(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()

    @staticmethod
    def get_product_data(product_id):
        product = Product.query.filter_by(prd_Id=product_id).first()
        if not product:
            return NotFoundProductError(f'Product ID = {product_id} not found')
        else:
            return product