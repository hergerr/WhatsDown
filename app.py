from flask import render_template, redirect, url_for, request, session, flash
from whatsdown import app, db
from whatsdown.forms import *
from whatsdown.models import *
from collections import Counter
from whatsdown.models import Administrator, FuneralHome, Buried, Funeral, Priest, Outfit, Container, PriestTemple, \
    Quarter, Tombstone
from werkzeug.security import generate_password_hash, check_password_hash
from whatsdown.utils import check_logged_in_user
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
    form = FilterForm()
    category = str(request.args["category"])
    phrase = str(request.args["phrase"])
    resource = request.query_string

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
        table = FuneralHome

    column_names = table.__table__.columns.keys()  # get columns names
    try:
        column_names.remove('id')
    except ValueError:
        pass

    try:
        column_names.remove('login')  # remove login if present
    except ValueError:
        pass

    try:
        column_names.remove('password')  # remove password if present
    except ValueError:
        pass

    if phrase == "":  # no whooshee_search when empty string is provided
        records = table.query.all()
    else:
        records = table.query.whooshee_search(phrase).all()  # get table records containing phrase

    query_records = []  # list of dictionaries (dict = record) to store in session

    if category == "buried":  # having foreign keys
        for record in records:
            row = {}
            for column_name in column_names:
                data = record[column_name]
                if data is not None and data != "":
                    if column_name == "outfit_id":
                        data = repr(Outfit.query.filter_by(id=data).first())
                    elif column_name == "container_id":
                        data = repr(Container.query.filter_by(id=data).first())
                    elif column_name == "quarter_id":
                        data = repr(Quarter.query.filter_by(id=data).first())
                    elif column_name == "funeral_id":
                        data = repr(Funeral.query.filter_by(id=data).first())
                    row[column_name] = str(data)
                else:
                    row[column_name] = "brak"

            row["outfit"] = row.pop("outfit_id")
            row["container"] = row.pop("container_id")
            row["quarter"] = row.pop("quarter_id")
            row["funeral"] = row.pop("funeral_id")
            query_records.append(row)

        column_names[column_names.index("outfit_id")] = "outfit"
        column_names[column_names.index("container_id")] = "container"
        column_names[column_names.index("quarter_id")] = "quarter"
        column_names[column_names.index("funeral_id")] = "funeral"

    elif category == "funeral":  # having foreign keys
        for record in records:
            row = {}
            for column_name in column_names:
                data = record[column_name]
                if data is not None and data != "":
                    if column_name == "funeral_home_id":
                        data = repr(FuneralHome.query.filter_by(id=data).first())
                    elif column_name == "priest_temple_id":
                        data = repr(PriestTemple.query.filter_by(id=data).first())
                    row[column_name] = str(data)
                else:
                    row[column_name] = "brak"

            row["funeral_home"] = row.pop("funeral_home_id")
            row["priest & temple"] = row.pop("priest_temple_id")
            query_records.append(row)

        column_names[column_names.index("funeral_home_id")] = "funeral_home"
        column_names[column_names.index("priest_temple_id")] = "priest & temple"

    elif category == "quarter":  # having foreign keys
        for record in records:
            row = {}
            for column_name in column_names:
                data = record[column_name]
                if data is not None and data != "":
                    if column_name == "cemetery_id":
                        data = repr(Cemetery.query.filter_by(id=data).first())
                    elif column_name == "tombstone_id":
                        data = repr(Tombstone.query.filter_by(id=data).first())
                    row[column_name] = str(data)
                else:
                    row[column_name] = "brak"

            row["cemetery"] = row.pop("cemetery_id")
            row["tombstone"] = row.pop("tombstone_id")
            query_records.append(row)

        column_names[column_names.index("cemetery_id")] = "cemetery"
        column_names[column_names.index("tombstone_id")] = "tombstone"
    else:  # no foreign keys
        for record in records:
            row = {}
            for column_name in column_names:
                data = record[column_name]
                if data is not None and data != "":
                    row[column_name] = str(data)
                else:
                    row[column_name] = "brak"
            query_records.append(row)

    session['column_names'] = column_names
    session['query_records'] = query_records

    return render_template('search.html', column_names=column_names, query_records=query_records, resource=resource,
                           form=form)


@app.route('/search/<string:resource>/filter', methods=['GET'])
def filter(resource):
    form = FilterForm()
    text = str(request.args["text"])
    filtered_records = []
    column_names = session.get('column_names', None)
    query_records = session.get('query_records', None)

    if text == "":
        filtered_records = query_records
    else:
        for record in query_records:
            for column_name in column_names:
                data = record[column_name]
                if data != "brak" and text.casefold() in str(data).casefold():
                    filtered_records.append(record)
                    break

    return render_template('filter.html', column_names=column_names, filtered_records=filtered_records,
                           resource=resource, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'logged' in session:
        if 'admin' in session:
            return redirect('/admin')
        elif 'user' in session:
            return redirect(url_for('dashboard'))

    session.permanent = True
    if form.validate_on_submit():
        admin = Administrator.query.filter_by(login=form.username.data).first()
        user = FuneralHome.query.filter_by(login=form.username.data).first()
        if admin:
            if check_password_hash(admin.password, form.password.data):
                session['logged'] = True
                session['admin'] = True
                return redirect('/admin')
            else:
                flash('Wrong password')
        elif user:
            if check_password_hash(user.password, form.password.data):
                session['logged'] = True
                session['user'] = True
                session['username'] = user.name
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password')
        else:
            flash('No such username')

    return render_template('login.html', form=form)


@app.route('/statistics')
def statistics():
    most_exclusive_priests = Priest.query.order_by(Priest.price).all()

    most_exclusive_priest = 'brak kapłanów'
    if len(most_exclusive_priests) != 0:
        most_exclusive_priest = most_exclusive_priests[-1]


    funeral_houses = FuneralHome.query.all()
    avg_fun_house_price = 0
    if len(funeral_houses) != 0:
        sum_price = 0
        for funeral_house in funeral_houses:
            sum_price += funeral_house.price
        avg_fun_house_price = sum_price / len(funeral_houses)

    buried_number = len(Buried.query.all())

    outfits = Outfit.query.all()
    most_popular_outfit_brand = ['brak strojów', 0]

    if len(outfits) != 0:
        counter = Counter([brand.brand for brand in outfits])
        most_popular_outfit_brand = counter.most_common(1)[0]

    most_popular_container_type = ['brak pojemników', 0]
    containers = Container.query.all()

    if len(containers) != 0:
        counter = Counter([container.type_of_container for container in containers])
        most_popular_container_type = counter.most_common(1)[0]

    most_expensive_funeal = 0
    funerals = Funeral.query.order_by(Funeral.total_price).all()
    if len(funerals):
        most_expensive_funeal = funerals[-1].total_price

    burieds = Buried.query.all()
    most_popular_cause_of_death = ['brak pochowanych', 'brak danych']
    if len(burieds) != 0:
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
        if form.special_key.data == 'admin':
            hashed_password = generate_password_hash(form.password.data, method='sha256')

            if Administrator.query.filter_by(login=form.username.data).first() or FuneralHome.query.filter_by(login=form.username.data).first():
                flash('This user already exists')
            else:
                new_admin = Administrator(login=form.username.data, password=hashed_password)
                db.session.add(new_admin)
                db.session.commit()
                flash('New admin created')

        else:
            flash('Wrong admin code')

    return render_template('signup-admin.html', form=form)


@app.route('/signup-user', methods=['GET', 'POST'])
def signup_user():
    form = RegisterUserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        if Administrator.query.filter_by(login=form.username.data).first() or FuneralHome.query.filter_by(login=form.username.data).first():
            flash('This user already exists')
        else:
            new_user = FuneralHome(login=form.username.data, password=hashed_password, name=form.name.data,
                                   voivodeship=form.voivodeship.data, county=form.county.data,
                                   locality=form.locality.data,
                                   phone=form.phone.data, price=form.price.data)
            db.session.add(new_user)
            db.session.commit()
            flash('New funeral agency created')

    return render_template('signup-user.html', form=form)


@app.route('/dashboard', methods=['POST', 'GET'])
@check_logged_in_user
def dashboard():
    edit_user_details = EditUserForm()
    current_user = FuneralHome.query.filter_by(name=session['username']).first()

    if request.method == 'POST':
        if edit_user_details.validate_on_submit():
            current_user.name = edit_user_details.name.data
            current_user.voivodeship = edit_user_details.voivodeship.data
            current_user.county = edit_user_details.county.data
            current_user.locality = edit_user_details.locality.data
            current_user.phone = edit_user_details.phone.data
            current_user.price = edit_user_details.price.data
            db.session.commit()
            session['username'] = current_user.name
        else:
            flash('Form invalid. Pass all data')

    return render_template('dashboard.html', edit_user_details=edit_user_details, current_user=current_user)


@app.route('/dashboard/buried', methods=['GET', 'POST'])
@check_logged_in_user
def user_buried():
    delete_record_form = DeleteRecordForm()
    buried_form = AddBuriedForm()
    edit_buried_form = EditBuriedForm()
    set_tombstone_form = SetTombstone()

    if request.method == 'POST':
        if edit_buried_form.validate_on_submit():

            buried_id = edit_buried_form.id.data
            buried_to_edit = Buried.query.filter_by(id=buried_id).first()

            # change funeral total price when buried is deleted
            funeral = Funeral.query.filter_by(id=buried_to_edit.funeral_id).first()
            funeral.total_price = funeral.total_price - buried_to_edit.container.price - buried_to_edit.outfit.price - buried_to_edit.quarter.price

            if edit_buried_form.birth_date.data and edit_buried_form.death_date.data:
                if edit_buried_form.birth_date.data > edit_buried_form.death_date.data:
                    flash('Wrong birth and death date')

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

            funeral.total_price = funeral.total_price + buried_to_edit.container.price + buried_to_edit.outfit.price + buried_to_edit.quarter.price

            db.session.commit()

        elif delete_record_form.validate_on_submit():
            buried_id = delete_record_form.id.data
            buried_to_delete = Buried.query.filter_by(id=buried_id).first()

            # change funeral total price when buried is deleted
            funeral = Funeral.query.filter_by(id=buried_to_delete.funeral_id).first()
            funeral.total_price = funeral.total_price - buried_to_delete.container.price - buried_to_delete.outfit.price - buried_to_delete.quarter.price

        
            quarter_id = buried_to_delete.quarter_id
            people_in_quarter = Buried.query.filter_by(quarter_id=quarter_id).all()
            if len(people_in_quarter) <= 1:
                quarter_to_free = Quarter.query.filter_by(id=quarter_id).first()
                quarter_to_free.tombstone = None

            if len(funeral.buried) <= 1:
                db.session.delete(funeral)

            db.session.delete(buried_to_delete)
            db.session.commit()


        elif buried_form.validate_on_submit():
            if edit_buried_form.birth_date.data and edit_buried_form.death_date.data:
                if buried_form.birth_date.data > buried_form.death_date.data:
                    flash('Wrong birth and death date')

            new_buried = Buried(first_name=buried_form.first_name.data, last_name=buried_form.last_name.data,
                                birth_date=buried_form.birth_date.data, death_date=buried_form.death_date.data,
                                cause_of_death=buried_form.cause_of_death.data, outfit_id=buried_form.outfit.data.id,
                                container_id=buried_form.container.data.id, quarter_id=buried_form.quarter.data.id,
                                funeral_id=buried_form.funeral.data.id)
            db.session.add(new_buried)
            db.session.commit()
            # must be after commit, otherwise doesnt see it
            new_buried.funeral.total_price = new_buried.funeral.total_price + new_buried.container.price + new_buried.outfit.price + new_buried.quarter.price
            db.session.commit()

        elif set_tombstone_form.validate_on_submit():
            quarter_id = set_tombstone_form.quarter.data.id
            quarter_to_set_on = Quarter.query.filter_by(id=quarter_id).first()
            quarter_to_set_on.tombstone = set_tombstone_form.tombstone.data
            db.session.commit()
            return redirect(url_for('user_buried'))

    buried = Buried.query.join(Funeral).join(FuneralHome).filter_by(name=session['username']).all()
    buried_header = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'cause_of_death', 'quarter',
                     'funeral', 'container', 'outfit']

    return render_template('user_buried.html', buried_form=buried_form, buried=buried,
                           buried_header=buried_header, delete_record_form=delete_record_form,
                           edit_buried_form=edit_buried_form, set_tombstone_form=set_tombstone_form)


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
            funeral_to_edit.date = edit_funeral_form.date.data
            funeral_to_edit.priest_temple = edit_funeral_form.priest_temple.data
            db.session.commit()

        elif delete_record_form.validate_on_submit():
            funeral_id = delete_record_form.id.data
            funeral_to_delete = Funeral.query.filter_by(id=funeral_id).first()
            buried_in_funeral = Buried.query.filter_by(funeral_id=funeral_id).all()
            for person in buried_in_funeral:
                quarter_id = person.quarter_id
                people_in_quarter = Buried.query.filter_by(quarter_id=quarter_id).all()
                if len(people_in_quarter) <= 1:
                    quarter_to_free = Quarter.query.filter_by(id=quarter_id).first()
                    quarter_to_free.tombstone = None
            db.session.delete(funeral_to_delete)
            db.session.commit()

        elif funeral_form.validate_on_submit():
            new_funeral = Funeral(date=funeral_form.date.data, priest_temple=funeral_form.priest_temple.data,
                                  funeral_home=FuneralHome.query.filter_by(name=session['username']).first())

            new_funeral.total_price = 0
            db.session.add(new_funeral)
            db.session.commit()
            # need to be after commit, otherwise doesnt see any attribute
            new_funeral.total_price = new_funeral.priest_temple.priest.price + new_funeral.funeral_home.price
            db.session.commit()

            return redirect(url_for('user_buried'))

        else:
            print('Form not valid')

    funerals = Funeral.query.join(FuneralHome).filter(FuneralHome.name == session['username']).all()
    funeral_header = ['id', 'date', 'total_price', 'buried on this funeral', 'priest and temple']

    return render_template('user_funerals.html', funeral_form=funeral_form, funerals=funerals,
                           funeral_header=funeral_header, delete_record_form=delete_record_form,
                           edit_funeral_form=edit_funeral_form)


if __name__ == '__main__':
    app.run(debug=True)
