from whatsdown import db
from flask_login import UserMixin


class Administrator(db.Model, UserMixin):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)

