from app import db, User
from werkzeug.security import generate_password_hash
from app import app

def create_admin():
    with app.app_context():
        # Sprawdź, czy istnieje użytkownik z rolą admin
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            # Utwórz administratora
            username = 'admin'
            password = 'admin_password'
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            admin_user = User(username=username, password=hashed_password, role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin()
