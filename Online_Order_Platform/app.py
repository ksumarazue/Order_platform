from flask import Flask
from database import db


app = Flask(__name__)
app.secret_key = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Order_Platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(debug=True)