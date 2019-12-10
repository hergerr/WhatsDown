from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SelectField
from .models import FuneralHome, Quarter, Funeral, Container, Outfit, PriestTemple, Tombstone
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Optional
from wtforms.fields.html5 import IntegerField, DateField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


class RegisterAdminForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    special_key = PasswordField('admin code', validators=[InputRequired()])


class RegisterUserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    voivodeship = SelectField('voivodeship', choices=[('Dolnośląskie', 'Dolnośląskie'),
                                                      ('Kujawsko-Pomorskie', 'Kujawsko-Pomorskie'),
                                                      ('Lubelskie', 'Lubelskie'), ('Łódzkie', 'Łódzkie'),
                                                      ('Małopolskie', 'Małopolskie'), ('Mazowieckie', 'Mazowieckie'),
                                                      ('Opolskie', 'Opolskie'), ('Podkarpackie', 'Podkarpackie'),
                                                      ('Podlaskie', 'Podlaskie'), ('Pomorskie', 'Pomorskie'),
                                                      ('Śląskie', 'Śląskie'), ('Świętokrzyskie', 'Świętokrzyskie'),
                                                      ('Warmińsko-Mazurskie', 'Warmińsko-Mazurskie'),
                                                      ('Wielkopolskie', 'Wielkopolskie'),
                                                      ('Zachodniopomorskie', 'Zachodniopomorskie')],
                              validators=[InputRequired()])
    county = StringField('county', validators=[InputRequired()])
    locality = StringField('locality', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    price = IntegerField('price', validators=[InputRequired()])


class SearchForm(FlaskForm):
    phrase = StringField('Enter the phrase you want to search for or leave the field empty to see all the contents')
    category = SelectField('Choose the category you want to search in', choices=[('buried', 'Buried'),
                                                                                 ('funeral', 'Funeral'),
                                                                                 ('cemetery', 'Cemetery'),
                                                                                 ('quarter', 'Quarter'),
                                                                                 ('outfit', 'Outfit'),
                                                                                 ('tombstone', 'Tombstone'),
                                                                                 ('container', 'Container'),
                                                                                 ('priest', 'Priest'),
                                                                                 ('temple', 'Temple'),
                                                                                 ('funeral_home', 'Funeral home')],
                           validators=[InputRequired()])


class FilterForm(FlaskForm):
    text = StringField('Enter a phrase to filter the results or leave the field empty to unfilter')


class AddFuneralForm(FlaskForm):
    date = DateField('date', validators=[InputRequired()])
    priest_temple = QuerySelectField('priest and temple', query_factory=lambda: PriestTemple.query.all(),
                                     validators=[InputRequired()])


class AddBuriedForm(FlaskForm):
    first_name = StringField('first name', validators=[InputRequired()])
    last_name = StringField('last name', validators=[InputRequired()])
    birth_date = DateField('birth date', validators=[Optional()])
    death_date = DateField('death date', validators=[Optional()])
    cause_of_death = StringField('cause of death', validators=[Optional()])
    quarter = QuerySelectField('quarter', query_factory=lambda: Quarter.query.filter(Quarter.tombstone == None).all(),
                               validators=[InputRequired()])
    funeral = QuerySelectField('funeral', query_factory=lambda: Funeral.query.join(FuneralHome)
                               .filter_by(name=session['username']).all(), validators=[InputRequired()])
    container = QuerySelectField('container', query_factory=lambda: Container.query.all(), validators=[InputRequired()])
    outfit = QuerySelectField('outfit', query_factory=lambda: Outfit.query.all(), validators=[InputRequired()])


class SetTombstone(FlaskForm):
    quarter = QuerySelectField('quarter', query_factory=lambda: Quarter.query.filter(Quarter.tombstone == None).all(),
                               validators=[InputRequired()])
    tombstone = QuerySelectField('tombstone', query_factory=lambda: Tombstone.query.all(), validators=[InputRequired()])


class DeleteRecordForm(FlaskForm):
    id = IntegerField('ID', validators=[InputRequired()])


class EditBuriedForm(AddBuriedForm):
    id = IntegerField('ID', validators=[InputRequired()])


class EditFuneralForm(AddFuneralForm):
    id = IntegerField('ID', validators=[InputRequired()])


class EditUserForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    voivodeship = SelectField('voivodeship', choices=[('Dolnośląskie', 'Dolnośląskie'),
                                                      ('Kujawsko-Pomorskie', 'Kujawsko-Pomorskie'),
                                                      ('Lubelskie', 'Lubelskie'), ('Łódzkie', 'Łódzkie'),
                                                      ('Małopolskie', 'Małopolskie'), ('Mazowieckie', 'Mazowieckie'),
                                                      ('Opolskie', 'Opolskie'), ('Podkarpackie', 'Podkarpackie'),
                                                      ('Podlaskie', 'Podlaskie'), ('Pomorskie', 'Pomorskie'),
                                                      ('Śląskie', 'Śląskie'), ('Świętokrzyskie', 'Świętokrzyskie'),
                                                      ('Warmińsko-Mazurskie', 'Warmińsko-Mazurskie'),
                                                      ('Wielkopolskie', 'Wielkopolskie'),
                                                      ('Zachodniopomorskie', 'Zachodniopomorskie')],
                              validators=[InputRequired()])
    county = StringField('county', validators=[InputRequired()])
    locality = StringField('locality', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    price = IntegerField('price', validators=[InputRequired()])
