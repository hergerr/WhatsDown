from flask import render_template, redirect, url_for, session
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterAdminForm, RegisterUserForm, AddFuneralForm, AddBuriedForm
from whatsdown.models import Administrator, User, Buried, Funeral
from werkzeug.security import generate_password_hash, check_password_hash
from whatsdown.utils import check_logged_in_user


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
                session['logged'] = True
                session['admin'] = True
                return redirect('/admin')
        elif user:
            if check_password_hash(user.password, form.password.data):
                session['logged'] = True
                session['user'] = True
                session['username'] = user.name
                return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
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
@check_logged_in_user
def dashboard():
    funeral_form = AddFuneralForm()
    buried_form = AddBuriedForm()
    buried = Buried.query.join(Funeral).join(User).filter_by(name=session['username']).all()
    buried_header = ['quarter', 'funeral', 'container', 'outfit', 'first_name', 'last_name', 'birth_date', 'death_date',
                     'cause_of_death']

    funerals = Funeral.query.join(Buried).join(User).filter_by(name=session['username']).all()
    print(dir(funerals[0].buried[0]))
    funeral_header = ['date', 'total_price', 'buried', 'funeral_house']

    return render_template('dashboard.html', funeral_form=funeral_form, buried_form=buried_form, buried=buried,
                           buried_header=buried_header, funerals=funerals, funeral_header=funeral_header)


if __name__ == '__main__':
    app.run(debug=True)
