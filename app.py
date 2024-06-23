from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user.user import User
from models.database import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        flash('You need to be logged in as admin to access this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        user_id = request.form.get('user_id')

        if action == 'create':
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash(f'User {username} created successfully.', 'success')
        elif action == 'update':
            user_to_update = User.query.get(user_id)
            if username:
                user_to_update.username = username
            if password:
                user_to_update.password = generate_password_hash(password, method='pbkdf2:sha256')
            if role:
                user_to_update.role = role
            db.session.commit()
            flash(f'User {user_to_update.username} updated successfully.', 'success')
        elif action == 'delete':
            user_to_delete = User.query.get(user_id)
            db.session.delete(user_to_delete)
            db.session.commit()
            flash(f'User {user_to_delete.username} deleted successfully.', 'success')

    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/home')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.role == 'admin':
            return render_template('home.html', user=user, admin=True)
        elif user.role == 'client':
            return render_template('home.html', user=user, client=True)
        else:
            return render_template('home.html', user=user, client=False, admin=False)
    else:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
