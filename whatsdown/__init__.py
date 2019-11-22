from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin
from flask_admin.contrib.sqla import ModelView
from whatsdown.config import name, db_name, password
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# db and admin config
app.secret_key = 'w4lepsze'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(name, password, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
Migrate(app, db)
admin = flask_admin.Admin(app)

from .models import Administrator, User, Buried, Tombstone, Quarter, Priest, Temple, Cemetery, Outfit, Container, \
    Funeral, Priest_Temple


# makes connection between flask login and data in db
@login_manager.user_loader
def load_admin(user_id):
    return Administrator.query.get(int(user_id))


class CustomModelView(ModelView):
    def is_accessible(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return current_user.is_authenticated
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
admin.add_view(CustomModelView(Priest_Temple, db.session))