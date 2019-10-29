from flask import render_template, redirect, url_for
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterForm
from whatsdown.models import Administrator
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        admin = Administrator.query.filter_by(name=form.username.data).first()
        if admin:
            if check_password_hash(admin.password, form.password.data):
                login_user(admin, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return 'Invalid username or password'

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_admin = Administrator(name=form.username.data, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        return 'Created new user'
    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
