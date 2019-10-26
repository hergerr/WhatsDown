import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import name, db_name, password
import flask_admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.secret_key = 'w4lepsze'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(name, password, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
from .models import Administrator

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = flask_admin.Admin(app)
admin.add_view(ModelView(Administrator, db.session))
