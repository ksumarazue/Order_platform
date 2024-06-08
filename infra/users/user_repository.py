from ..database import db
from ..users.user import User



class InvalidUserError(Exception):
    pass


class NotFoundUserError(Exception):
    pass


class UserRepository:
    def get_all_users(self):
        return User.query.all()

    def add_user(self, name: str, email: str, password: str, group: str):
        if not name or not email or not password or not group:
            raise InvalidUserError("Invalid expense data")
        print(name, email, password, group)
        new_user = User(name=name, email=email, password=password, group=group)
        db.session.add(new_user)
        db.session.commit()

    def update_user(self, id, name, email, password, group):
        user = self.get_user_data(id)
        if not name or not email or not password or not group:
            raise InvalidUserError('Invalid user data')
        if user:
            user.name = name
            user.email = email
            user.password = password
            user.group = group
            db.session.commit()

    @staticmethod
    def get_user_data(id):
        print(f'get user data {id}')
        user = User.query.filter_by(id=id).first()
        if not user:
            return NotFoundUserError(f'User ID = {id} not found')
        else:
            return user


    def delete_user(self, id):
        user = self.get_user_data(id)
        if user:
            db.session.delete(user)
            db.session.commit()