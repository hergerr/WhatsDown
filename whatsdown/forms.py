from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired


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
    price = IntegerField('price', validators=[InputRequired()])


class SearchForm(FlaskForm):
    phrase = StringField('Enter the phrase you want to search for', validators=[InputRequired()])
    category = SelectField('Choose the category you want to search in', choices=[('buried', 'Buried'), ('funeral', 'Funeral'), ('cemetery', 'Cemetery'),
                                                ('quarter', 'Quarter'), ('outfit', 'Outfit'),
                                                ('tombstone', 'Tombstone'), ('container', 'Container'),
                                                ('priest', 'Priest'), ('temple', 'Temple'), ('funeral_home',
                                                                                             'Funeral home')],
                           validators=[InputRequired()])
