from flask import render_template, redirect, url_for, session, request
from whatsdown import app, db
from whatsdown.forms import LoginForm, RegisterAdminForm, RegisterUserForm, AddFuneralForm, AddBuriedForm, \
    DeleteRecordForm, EditBuriedForm, EditFuneralForm
from collections import Counter
from whatsdown.models import Administrator, FuneralHome, Buried, Funeral, Priest, Outfit, Container
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
        user = FuneralHome.query.filter_by(login=form.username.data).first()
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


@app.route('/statistics')
def statistics():
    most_exclusive_priest = Priest.query.order_by(Priest.price)[-1]

    funeral_houses = FuneralHome.query.all()
    sum_price = 0
    for funeral_house in funeral_houses:
        sum_price += funeral_house.price
    avg_fun_house_price = sum_price / len(funeral_houses)

    buried_number = len(Buried.query.all())

    outfits = Outfit.query.all()
    counter = Counter([brand.brand for brand in outfits])
    most_popular_outfit_brand = counter.most_common(1)[0]

    containers = Container.query.all()
    counter = Counter([container.type_of_container for container in containers])
    most_popular_container_type = counter.most_common(1)[0]

    most_expensive_funeal = Funeral.query.order_by(Funeral.total_price)[-1]

    burieds = Buried.query.all()  # Form F.M: it's on purpose, late i use it in loop and i want do distinguish it
    counter = Counter([buried.cause_of_death for buried in burieds])
    most_popular_cause_of_death = counter.most_common(1)[0]

    return render_template('statistics.html', most_exclusive_priest=most_exclusive_priest,
                           avg_fun_house_price=avg_fun_house_price, buried_number=buried_number,
                           most_popular_outfit_brand=most_popular_outfit_brand,
                           most_popular_container_type=most_popular_container_type,
                           most_expensive_funeal=most_expensive_funeal,
                           most_popular_cause_of_death=most_popular_cause_of_death)


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
        print(form.phone.data)
        new_user = FuneralHome(login=form.username.data, password=hashed_password, name=form.name.data,
                               voivodeship=form.voivodeship.data, county=form.county.data, locality=form.locality.data,
                               phone=form.phone.data)
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
        if edit_buried_form.validate_on_submit():

            buried_id = edit_buried_form.id.data
            buried_to_edit = Buried.query.filter_by(id=buried_id).first()

            buried_to_edit.first_name = edit_buried_form.first_name.data
            buried_to_edit.last_name = edit_buried_form.last_name.data
            buried_to_edit.birth_date = edit_buried_form.birth_date.data
            buried_to_edit.death_date = edit_buried_form.death_date.data
            buried_to_edit.cause_of_death = edit_buried_form.cause_of_death.data
            buried_to_edit.outfit_id = edit_buried_form.outfit.data.id
            buried_to_edit.container_id = edit_buried_form.container.data.id
            buried_to_edit.quarter_id = edit_buried_form.quarter.data.id
            buried_to_edit.funeral_id = edit_buried_form.funeral.data.id

            db.session.commit()

        elif delete_record_form.validate_on_submit():
            buried_id = delete_record_form.id.data
            buried_to_delete = Buried.query.filter_by(id=buried_id).first()
            db.session.delete(buried_to_delete)
            db.session.commit()

        elif buried_form.validate_on_submit():
            new_buried = Buried(first_name=buried_form.first_name.data, last_name=buried_form.last_name.data,
                                birth_date=buried_form.birth_date.data, death_date=buried_form.death_date.data,
                                cause_of_death=buried_form.cause_of_death.data, outfit_id=buried_form.outfit.data.id,
                                container_id=buried_form.container.data.id, quarter_id=buried_form.quarter.data.id,
                                funeral_id=buried_form.funeral.data.id)
            db.session.add(new_buried)
            db.session.commit()

    buried = Buried.query.join(Funeral).join(FuneralHome).filter_by(name=session['username']).all()
    buried_header = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'cause_of_death', 'quarter',
                     'funeral', 'container', 'outfit']

    return render_template('user_buried.html', buried_form=buried_form, buried=buried,
                           buried_header=buried_header, delete_record_form=delete_record_form,
                           edit_buried_form=edit_buried_form)


@app.route('/dashboard/funerals', methods=['GET', 'POST'])
@check_logged_in_user
def user_funerals():
    funeral_form = AddFuneralForm()
    delete_record_form = DeleteRecordForm()
    edit_funeral_form = EditFuneralForm()

    if request.method == 'POST':
        if edit_funeral_form.validate_on_submit():
            funeral_id = edit_funeral_form.id.data
            funeral_to_edit = Funeral.query.filter_by(id=funeral_id).first()

            if not edit_funeral_form.buried.data:
                edit_funeral_form.buried.data = ['']


            # TODO dodac sprawdzenie czy w bazie jest takie id
            funeral_to_edit.date = edit_funeral_form.date.data
            funeral_to_edit.total_price = edit_funeral_form.total_price.data
            funeral_to_edit.buried = [edit_funeral_form.buried.data]
            funeral_to_edit.priest_temple = edit_funeral_form.priest_temple.data

            db.session.commit()

        elif delete_record_form.validate_on_submit():
            funeral_id = delete_record_form.id.data
            funeral_to_delete = Funeral.query.filter_by(id=funeral_id).first()
            db.session.delete(funeral_to_delete)
            db.session.commit()

        elif funeral_form.validate_on_submit():
            if not funeral_form.buried.data:
                funeral_form.buried.data = []

            new_funeral = Funeral(date=funeral_form.date.data, total_price=funeral_form.total_price.data,
                                  buried=funeral_form.buried.data,
                                  funeral_home_id=FuneralHome.query.filter_by(name=session['username']).first().id,
                                  priest_temple=funeral_form.priest_temple.data)
            db.session.add(new_funeral)
            db.session.commit()

        else:
            print('Form not valid')

    funerals = Funeral.query.join(FuneralHome).filter(FuneralHome.name == session['username']).all()
    funeral_header = ['id', 'date', 'total_price', 'buried', 'priest and temple']

    return render_template('user_funerals.html', funeral_form=funeral_form, funerals=funerals,
                           funeral_header=funeral_header, delete_record_form=delete_record_form,
                           edit_funeral_form=edit_funeral_form)


if __name__ == '__main__':
    app.run(debug=True)
