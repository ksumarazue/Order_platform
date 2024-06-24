from models.order.order import Order, OrderItem
from models.product.product import Product
from models.database import db
from models.user.user import User


class OrderRepository:
    def calculate_cart_total(self, cart_items):
        product_ids = []
        for items in cart_items:
            product_ids.append(items['product_id'])
        products = self.get_cart_data(product_ids)

        total = 0
        for item in cart_items:
            product_id = item['product_id']
            product = None
            for p in products:
                if p.id == product_id:
                    product = p
                    break
            if product:
                product_price = product.price
            else:
                product_price = 0
            item_quantity = item['quantity']
            item_total = item_quantity * product_price
            total += item_total
        return total, products

    def confirm_cart(self, user_id, cart_items):
        order = Order(user_id=user_id, status='confirmed')
        db.session.add(order)
        db.session.commit()
        for item in cart_items:
            order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
            db.session.add(order_item)
        db.session.commit()
        return order

    @staticmethod
    def get_cart_data(product_ids):
        products_query = Product.query.filter(Product.id.in_(product_ids))
        products = products_query.all()
        return products

    def get_all_order_for_user(self, user):
        if user.role == 'client':
            orders = Order.query.filter_by(user_id=user.id).all()
        else:
            orders = Order.query.all()

        orders_with_users = []
        for order in orders:
            order_user = User.query.get(order.user_id)
            orders_with_users.append((order, order_user))
        return orders_with_users

    def get_order_detail(self, order_id):
        order = Order.query.get_or_404(order_id)
        order_user = User.query.get(order.user_id)
        return order, order_user