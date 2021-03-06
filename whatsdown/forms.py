from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SelectField
from .models import FuneralHome, Quarter, Funeral, Container, Outfit, PriestTemple, Tombstone
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Optional, EqualTo
from wtforms.fields.html5 import IntegerField, DateField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[InputRequired()],
                             render_kw={"placeholder": "Password"})


class RegisterAdminForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[InputRequired(), EqualTo('confirm',
                                                                              message='Passwords must match')],
                             render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password',  render_kw={"placeholder": "Repeat password"})
    special_key = PasswordField('admin code', validators=[InputRequired()],  render_kw={"placeholder": "Special key"})


class RegisterUserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[InputRequired(), EqualTo('confirm',
                                                                              message='Passwords must match')],
                             render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Repeat Password"})
    name = StringField('name', validators=[InputRequired()], render_kw={"placeholder": "Company name"})
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
    county = StringField('county', validators=[InputRequired()], render_kw={"placeholder": "County"})
    locality = StringField('locality', validators=[InputRequired()], render_kw={"placeholder": "Locality"})
    phone = StringField('phone', validators=[InputRequired()], render_kw={"placeholder": "Phone"})
    price = IntegerField('price', validators=[InputRequired()], render_kw={"placeholder": "Price"})


class SearchForm(FlaskForm):
    phrase = StringField(render_kw={"placeholder": "Enter the search phrase or leave the field empty"})
    category = SelectField(render_kw={"placeholder": "Choose the category you want to search in"}, choices=[
        ('buried', 'Buried'),
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
    text = StringField(render_kw={"placeholder": "Enter a phrase to filter"})


class AddFuneralForm(FlaskForm):
    date = DateField('date', validators=[InputRequired()])
    priest_temple = QuerySelectField('priest and temple', query_factory=lambda: PriestTemple.query.all(),
                                     validators=[InputRequired()])


class AddBuriedForm(FlaskForm):
    first_name = StringField('first name', validators=[InputRequired()], render_kw={"placeholder": "First name"})
    last_name = StringField('last name', validators=[InputRequired()], render_kw={"placeholder": "Last name"})
    birth_date = DateField('birth date', validators=[Optional()])
    death_date = DateField('death date', validators=[Optional()])
    cause_of_death = StringField('cause of death', validators=[Optional()], render_kw={"placeholder": "Cause of death"})
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
