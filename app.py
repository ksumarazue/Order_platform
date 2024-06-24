from flask import Flask

from controllers.order.order_view import order_blueprint
from controllers.product.product_view import product_blueprint
from models.database import db
from controllers.user.user_view import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


with app.app_context():
    db.create_all()

app.register_blueprint(user_blueprint, url_prefix='/')
app.register_blueprint(product_blueprint, url_prefix='/')
app.register_blueprint(order_blueprint, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)
