from flask import Flask, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin
from flask_admin.contrib.sqla import ModelView
from whatsdown.config import name, db_name, password
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# db and admin config
app.secret_key = 'w4lepsze'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(name, password, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
Migrate(app, db)
admin = flask_admin.Admin(app)

from .models import Administrator, User, Buried, Tombstone, Quarter, Priest, Temple, Cemetery, Outfit, Container, \
    Funeral


class CustomModelView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        else:
            return abort(404)


# here models are registered to admin
admin.add_view(CustomModelView(Administrator, db.session))
admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Buried, db.session))
admin.add_view(CustomModelView(Tombstone, db.session))
admin.add_view(CustomModelView(Quarter, db.session))
admin.add_view(CustomModelView(Priest, db.session))
admin.add_view(CustomModelView(Temple, db.session))
admin.add_view(CustomModelView(Cemetery, db.session))
admin.add_view(CustomModelView(Outfit, db.session))
admin.add_view(CustomModelView(Container, db.session))
admin.add_view(CustomModelView(Funeral, db.session))
