from flask import render_template, redirect, url_for
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterAdminForm, RegisterUserForm
from whatsdown.models import Administrator, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        admin = Administrator.query.filter_by(login=form.username.data).first()
        user = User.query.filter_by(login=form.username.data).first()
        if admin:
            if check_password_hash(admin.password, form.password.data):
                login_user(admin, remember=form.remember.data)
                return redirect('/admin')
        elif user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home_page'))
        else:
            return 'Invalid username or password'

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup-admin', methods=['GET', 'POST'])
def signup_admin():
    form = RegisterAdminForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_admin = Administrator(login=form.username.data, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        return 'New admin created'

    return render_template('signup-admin.html', form=form)


@app.route('/signup-user', methods=['GET', 'POST'])
def signup_user():
    form = RegisterUserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(login=form.username.data, password=hashed_password, name=form.name.data,
                        voivodeship=form.voivodeship.data, county=form.county.data, locality=form.locality.data,
                        phone=form.phone.data, price=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        return 'New funeral agency created'

    return render_template('signup-user.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
