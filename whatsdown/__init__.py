from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin
from flask_admin.contrib.sqla import ModelView
from whatsdown.config import name, db_name, password
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_whooshee import Whooshee


app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# db and admin config
app.secret_key = 'w4lepsze'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(name, password, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['WHOOSHEE_MIN_STRING_LEN'] = 1
app.config['WHOOSHEE_DIR'] = 'whooshee_indexes'

db = SQLAlchemy(app)
Migrate(app, db)
admin = flask_admin.Admin(app)

whooshee = Whooshee(app)
whooshee.reindex()

#app.jinja_env.add_extension('jinja2.ext.loopcontrols')


# @whooshee.register_model('name', 'voivodeship', 'county', 'locality', 'phone')
# @whooshee.register_model('manufacturer', 'material')
# @whooshee.register_model('voivodeship', 'county', 'locality', 'street', 'faith')
# @whooshee.register_model('type_of_clothing', 'size', 'brand', 'color')
# @whooshee.register_model('type_of_container', 'manufacturer', 'material')
# @whooshee.register_model('first_name', 'last_name', 'cause_of_death')
# @whooshee.register_model('title', 'first_name', 'last_name', 'religion')
# @whooshee.register_model('voivodeship', 'county', 'locality', 'religion', 'rank')


# makes connection between flask login and data in db
# @login_manager.user_loader
# def load_admin(user_id):
#     return Administrator.query.get(int(user_id))


# class CustomModelView(ModelView):
#     def is_accessible(self):
#         if hasattr(current_user, 'is_admin') and current_user.is_admin:
#             return current_user.is_authenticated
#         else:
#             return abort(404)


# from .models import Administrator, User, Buried, Tombstone, Quarter, Priest, Temple, Cemetery, Outfit, Container, \
#     Funeral

# here models are registered to admin
# admin.add_view(CustomModelView(Administrator, db.session))
# admin.add_view(CustomModelView(User, db.session))
# admin.add_view(CustomModelView(Buried, db.session))
# admin.add_view(CustomModelView(Tombstone, db.session))
# admin.add_view(CustomModelView(Quarter, db.session))
# admin.add_view(CustomModelView(Priest, db.session))
# admin.add_view(CustomModelView(Temple, db.session))
# admin.add_view(CustomModelView(Cemetery, db.session))
# admin.add_view(CustomModelView(Outfit, db.session))
# admin.add_view(CustomModelView(Container, db.session))
# admin.add_view(CustomModelView(Funeral, db.session))
