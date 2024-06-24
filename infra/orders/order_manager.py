from ..orders.order import Order
from ..database import db


class OrderRepository:
    def get_all_orders(self):
        return Order.query.all()


    # def create_order(self):
    #     pass