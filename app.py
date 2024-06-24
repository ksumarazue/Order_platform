from flask import Flask, render_template, url_for, redirect
from flask_login import logout_user

from controllers.user.user_views import user_bp
from controllers.order.order_view import order_bp
from controllers.product.product_view import product_bp
from controllers.login.auth_view import auth_bp
from infra.database import db

app = Flask(__name__)
app.secret_key = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Order_Platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)

# @app.route('/')
# def hello():
#     return 'Hello, World!'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth_bp.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))





if __name__ == '__main__':
    app.run(debug=True)