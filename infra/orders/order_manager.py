from ..orders.order import Order
from ..database import db


class InvalidOrderError(Exception):
    pass


class NotFoundOrderError(Exception):
    pass


class OrderRepository:
    def get_all_orders(self):
        return Order.query.all()


    # def create_order(self, user_name, ):


    # ord_id = db.Column(db.Integer, primary_key = True)
    # ord_UsrId = db.Column(db.Integer, nullable = False)
    # ord_UsrName = db.Column(db.String(20), nullable = False)
    # ord_Status = db.Column(db.String(20), nullable = False)