from flask import Flask
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

from .models import Administrator

# here models are registered to admin
admin.add_view(ModelView(Administrator, db.session))
