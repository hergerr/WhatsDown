from flask import render_template, redirect, url_for, session, request
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterAdminForm, RegisterUserForm, AddFuneralForm, AddBuriedForm, \
    DeleteRecordForm, EditBuriedForm
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
    return render_template('dashboard.html')


@app.route('/dashboard/buried', methods=['GET', 'POST'])
@check_logged_in_user
def user_buried():
    delete_record_form = DeleteRecordForm()
    buried_form = AddBuriedForm()
    edit_buried_form = EditBuriedForm()

    if request.method == 'POST':
        if delete_record_form.validate_on_submit():
            buried_id = delete_record_form.id.data
            buried_to_delete = Buried.query.filter_by(id=buried_id).first()
            db.session.delete(buried_to_delete)
            db.session.commit()

        if buried_form.validate_on_submit():
            new_buried = Buried(first_name=buried_form.first_name.data, last_name=buried_form.last_name.data,
                                birth_date=buried_form.birth_date.data, death_date=buried_form.death_date.data,
                                cause_of_death=buried_form.cause_of_death.data, outfit_id=buried_form.outfit.data.id,
                                container_id=buried_form.container.data.id, quarter_id=buried_form.quarter.data.id,
                                funeral_id=buried_form.funeral.data.id)
            db.session.add(new_buried)
            db.session.commit()

    buried = Buried.query.join(Funeral).join(User).filter_by(name=session['username']).all()
    buried_header = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'cause_of_death', 'quarter',
                     'funeral', 'container', 'outfit']

    return render_template('user_buried.html', buried_form=buried_form, buried=buried,
                           buried_header=buried_header, delete_record_form=delete_record_form,
                           edit_buried_form=edit_buried_form)


@app.route('/dashboard/funerals', methods=['GET', 'POST'])
@check_logged_in_user
def user_funerals():
    funeral_form = AddFuneralForm()
    funerals = Funeral.query.join(Buried).join(User).filter_by(name=session['username']).all()
    funeral_header = ['id', 'date', 'total_price', 'buried', 'funeral_house']

    delete_record_form = DeleteRecordForm()

    if request.method == 'POST':
        if delete_record_form.validate_on_submit():
            funeral_id = delete_record_form.id.data
            funeral_to_delete = Funeral.query.filter_by(id=funeral_id).first()
            db.session.delete(funeral_to_delete)
            db.session.commit()

    return render_template('user_funerals.html', funeral_form=funeral_form, funerals=funerals,
                           funeral_header=funeral_header, delete_record_form=delete_record_form)


if __name__ == '__main__':
    app.run(debug=True)
