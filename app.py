from flask import Flask
from models.database import db
from controllers.user.user_view import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
