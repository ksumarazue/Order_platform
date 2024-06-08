from ..users.user import User
from ...database import db


class InvalidExpenseError(Exception):
    pass


class NotFoundExpenseError(Exception):
    pass


class UserManager:
    def get_all_users(self):
        return User.query.all()

    def add_user(self, name: str, email: str, password: str, group: str):
        if not name or not email or not password or not group:
            raise InvalidExpenseError("Invalid expense data")
        new_user = User(user_name=name, user_email=email, user_password=password, user_group=group)
        db.session.add(new_user)
        db.session.commit()


    def update_user(self):
        pass