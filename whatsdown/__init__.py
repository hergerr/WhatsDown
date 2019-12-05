from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin
from whatsdown.config import name, db_name, password
from flask_bootstrap import Bootstrap
from flask_whooshee import Whooshee
from datetime import timedelta


app = Flask(__name__)
Bootstrap(app)

# db and admin config
app.secret_key = 'w4lepsze'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(name, password, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['WHOOSHEE_MIN_STRING_LEN'] = 1
app.config['WHOOSHEE_DIR'] = 'whooshee_indexes'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

db = SQLAlchemy(app)
Migrate(app, db)
admin = flask_admin.Admin(app)

whooshee = Whooshee(app)
whooshee.reindex()
