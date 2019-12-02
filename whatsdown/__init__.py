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
