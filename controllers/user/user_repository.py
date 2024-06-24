from werkzeug.security import generate_password_hash

from models.database import db
from models.user.user import User


class UserRepository:
    def get_all_users(self):
        return User.query.all()

    def create_user(self, username, password, role):
        if not username or not password or not role:
            pass
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

    def update_user(self, user_id, username, password, role):
        user = self.get_user_data(user_id)
        if not username or not password or not role:
            pass
        if user:
            if username:
                user.username = username
            if password:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                user.password = hashed_password
            if role:
                user.role = role
            db.session.commit()

    def delete_user(self, user_id):
        user = self.get_user_data(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def get_user_data(user_id):
        user = User.query.get(user_id)
        if not user:
            pass
        else:
            return user