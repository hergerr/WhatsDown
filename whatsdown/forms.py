from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, BooleanField
from .models import Buried, FuneralHome, Quarter, Funeral, Container, Outfit, PriestTemple
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import IntegerField, DateField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember me')


class RegisterAdminForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    special_key = PasswordField('admin code', validators=[InputRequired()])


class RegisterUserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    voivodeship = StringField('voivodeship', validators=[InputRequired()])
    county = StringField('county', validators=[InputRequired()])
    locality = StringField('locality', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])


class AddFuneralForm(FlaskForm):
    date = DateField('date')
    total_price = IntegerField('total price')
    buried = QuerySelectField('buried', query_factory=lambda: Buried.query.all(), allow_blank=True)
    priest_temple = QuerySelectField('priest and temple', query_factory=lambda: PriestTemple.query.all())


class AddBuriedForm(FlaskForm):
    first_name = StringField('first name')
    last_name = StringField('last name')
    birth_date = DateField('birth date')
    death_date = DateField('death date')
    cause_of_death = StringField('cause of death')
    quarter = QuerySelectField('quarter', query_factory=lambda: Quarter.query.all())
    funeral = QuerySelectField('funeral', query_factory=lambda: Funeral.query.join(FuneralHome)
                               .filter_by(name=session['username']).all())
    container = QuerySelectField('container', query_factory=lambda: Container.query.all())
    outfit = QuerySelectField('outfit', query_factory=lambda: Outfit.query.all())


class DeleteRecordForm(FlaskForm):
    id = IntegerField('ID', validators=[InputRequired()])


# TODO ponizsze klasy moga dziedziczyc po formach do dodania
class EditBuriedForm(FlaskForm):
    id = IntegerField('ID', validators=[InputRequired()])
    first_name = StringField('first name')
    last_name = StringField('last name')
    birth_date = DateField('birth date', format='%Y-%m-%d')
    death_date = DateField('death date', format='%Y-%m-%d')
    cause_of_death = StringField('cause of death')
    quarter = QuerySelectField('quarter', query_factory=lambda: Quarter.query.all())
    funeral = QuerySelectField('funeral', query_factory=lambda: Funeral.query.join(FuneralHome)
                               .filter_by(name=session['username']).all())
    container = QuerySelectField('container', query_factory=lambda: Container.query.all())
    outfit = QuerySelectField('outfit', query_factory=lambda: Outfit.query.all())


class EditFuneralForm(FlaskForm):
    id = IntegerField('ID', validators=[InputRequired()])
    date = DateField('date')
    total_price = IntegerField('total price')
    buried = QuerySelectField('buried', query_factory=lambda: Buried.query.all(), allow_blank=True)
    priest_temple = QuerySelectField('priest and temple', query_factory=lambda: PriestTemple.query.all())
