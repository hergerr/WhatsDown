from flask import render_template, redirect, url_for, request
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterAdminForm, RegisterUserForm, SearchForm
from whatsdown.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from flask_whooshee import *

ws = WhoosheeQuery.whooshee_search


@app.route('/', methods=['GET'])
def home_page():
    form = SearchForm()
    if form.validate_on_submit():
        redirect(url_for('search'))
    return render_template('home.html', form=form)


@app.route('/search', methods=['GET'])
def search():
    category = str(request.args["category"])
    phrase = str(request.args["phrase"])

    table = Buried
    if category == "buried":
        table = Buried
    elif category == "funeral":
        table = Funeral
    elif category == "cemetery":
        table = Cemetery
    elif category == "quarter":
        table = Quarter
    elif category == "outfit":
        table = Outfit
    elif category == "tombstone":
        table = Tombstone
    elif category == "container":
        table = Container
    elif category == "priest":
        table = Priest
    elif category == "temple":
        table = Temple
    elif category == "funeral_home":
        table = User

    column_names = table.__table__.columns.keys()  # get columns names
    records = table.query.whooshee_search(phrase).all()  # get table records

    DATA = []

    for record in records:
        row = {}
        for column_name in column_names:
            row[column_name] = record[column_name]
        DATA.append(row)

    return render_template('search.html', column_names=column_names, records=records)


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
                        phone=form.phone.data, price=form.price.data)
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