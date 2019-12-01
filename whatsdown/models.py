from whatsdown import db
from flask import abort
from flask_login import LoginManager, UserMixin, current_user
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import date, datetime
from whatsdown import admin, login_manager, whooshee
from flask_admin.contrib.sqla import ModelView

# czy 'data' to to samo co "data"?
# w szczególności przy oznaczaniu rodziców i dzieci w kluczach obcych ('parent) vs ("parent")


class Administrator(db.Model, UserMixin):
    __tablename__ = 'administrator'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Administrator {self.id}, login {self.login}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('name', 'voivodeship', 'county', 'locality', 'phone')
class User(db.Model, UserMixin):
    # connected with funeral o-t-m
    # atributes
    __tablename__ = 'funeral_home'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(30), unique=True)
    voivodeship = db.Column(db.Text)
    county = db.Column(db.Text)
    locality = db.Column(db.Text)
    phone = db.Column(db.Text)
    price = db.Column(db.Integer)
    login = db.deferred(db.Column(db.String(30), nullable=False, unique=True))
    password = db.deferred(db.Column(db.String(30), nullable=False))

    # bidirectional relationships
    funerals = relationship("Funeral", back_populates="funeral_home")

    def __repr__(self):
        return f'Dom pogrzebowy {self.name}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('manufacturer', 'material')
class Tombstone(db.Model):  # connected with quarter o-t-m
    # atributes
    __tablename__ = 'tombstone'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    manufacturer = db.Column(db.Text)
    material = db.Column(db.Text)
    price = db.Column(db.Integer)

    # relationships
    quarter = relationship("Quarter", back_populates="tombstone")

    def __repr__(self):
        return f'Nagrobek marki {self.manufacturer}, model {self.material}'

    def __getitem__(self, field):
        return self.__dict__[field]


class Quarter(db.Model):
    # connected with cemetary o-t-m
    # connected with tombstone o-t-m
    # connected with buried m-t-o
    # atributes
    __tablename__ = 'quarter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)
    price = db.Column(db.Integer)

    # foreign keys
    cemetery_id = db.Column(db.Integer, db.ForeignKey('cemetery.id'), nullable=False)
    tombstone_id = db.Column(db.Integer, db.ForeignKey('tombstone.id'), nullable=True)

    # relationships
    cemetery = relationship("Cemetery", back_populates="quarters")
    buried = relationship("Buried", back_populates="quarter")
    tombstone = relationship("Tombstone", back_populates="quarter")

    def __repr__(self):
        return f'Kwatera na cmentarzu nr {self.cemetery_id}, x={self.x_coord}, y={self.y_coord}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('voivodeship', 'county', 'locality', 'street', 'faith')
class Cemetery(db.Model):
    # connected with quarter m-t-o
    # atributes
    __tablename__ = 'cemetery'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    voivodeship = db.Column(db.Text)
    county = db.Column(db.Text)
    locality = db.Column(db.Text)
    street = db.Column(db.Text)
    faith = db.Column(db.Text)

    # bidirectional relationships
    quarters = relationship("Quarter", back_populates="cemetery")

    def __repr__(self):
        return f'Cmentarz w woj. {self.voivodeship}, powiat {self.county}, miejscowość {self.locality}, ulica {self.street}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('type_of_clothing', 'size', 'brand', 'color')
class Outfit(db.Model):
    # connected with buried m-t-o

    # atributes
    __tablename__ = 'outfit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type_of_clothing = db.Column(db.Text)
    size = db.Column(db.Text)
    brand = db.Column(db.Text)
    color = db.Column(db.Text)
    price = db.Column(db.Integer)

    # relationships
    buried = relationship("Buried", back_populates="outfit")

    def __repr__(self):
        return f'{self.type_of_clothing}, marki  {self.brand}, rozmiar {self.size}, w kolorze {self.color}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('type_of_container', 'manufacturer', 'material')
class Container(db.Model):
    # connected with buried m-t-o

    # atributes
    __tablename__ = 'container'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type_of_container = db.Column(db.Text)
    manufacturer = db.Column(db.Text)
    material = db.Column(db.Text)
    price = db.Column(db.Integer)

    # relationships
    buried = relationship("Buried", back_populates="container")

    def __repr__(self):
        return f'Pojemnik {self.manufacturer}, wykonany z {self.material}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('first_name', 'last_name', 'cause_of_death')
class Buried(db.Model):
    # connected with outfit o-t-m
    # connected with container o-t-m
    # connected with quarter o-t-m

    # atributes
    __tablename__ = 'buried'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    birth_date = db.Column(db.DateTime())
    death_date = db.Column(db.DateTime())
    cause_of_death = db.Column(db.Text)

    # foreign keys
    outfit_id = db.Column(db.Integer, ForeignKey('outfit.id'), nullable=True)
    container_id = db.Column(db.Integer, ForeignKey('container.id'), nullable=True)
    quarter_id = db.Column(db.Integer, ForeignKey('quarter.id'), nullable=False)
    funeral_id = db.Column(db.Integer, ForeignKey('funeral.id'), nullable=False)

    # bidirectional relationships
    quarter = relationship("Quarter", back_populates="buried")
    funeral = relationship("Funeral", back_populates="buried")
    container = relationship("Container", back_populates="buried")
    outfit = relationship("Outfit", back_populates="buried")

    def __repr__(self):
        return f'Pochowany {self.first_name} {self.last_name}'

    def __getitem__(self, field):
        return self.__dict__[field]


class Funeral(db.Model):
    # connected with funeral_home o-t-m
    # connected with buried m-t-o
    # connected with (priest&temple) o-t-m

    # atributes
    __tablename__ = 'funeral'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    total_price = db.Column(db.Integer)

    # foreign keys
    funeral_home_id = db.Column(db.Integer, ForeignKey('funeral_home.id'), nullable=True)

    # bidirectional relationships
    buried = relationship("Buried", back_populates="funeral")
    funeral_home = relationship("User", back_populates="funerals")

    def __repr__(self):
        return f'Pogrzeb nr {self.id}'

    def __getitem__(self, field):
        return self.__dict__[field]

    # table many-to-many
    priest_temple = db.Table('priest_temple',
                             db.Column('priest_id', db.Integer(), db.ForeignKey('priest.id'), primary_key=True),
                             db.Column('temple_id', db.Integer(), db.ForeignKey('temple.id'), primary_key=True))


@whooshee.register_model('title', 'first_name', 'last_name', 'religion')
class Priest(db.Model):
    # connected with temple m-t-m

    # atributes
    __tablename__ = 'priest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    religion = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __repr__(self):
        return f'Kapłan {self.first_name}, {self.last_name}'

    def __getitem__(self, field):
        return self.__dict__[field]


@whooshee.register_model('voivodeship', 'county', 'locality', 'religion', 'rank')
class Temple(db.Model):
    # connected with priest m-t-m

    # atributes
    __tablename__ = 'temple'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    voivodeship = db.Column(db.Text)
    county = db.Column(db.Text)
    locality = db.Column(db.Text)
    religion = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    rank = db.Column(db.Text)

    def __repr__(self):
        return f'Swiątynia wyznania {self.religion}, umiejscowiona w {self.voivodeship}, {self.county}, {self.locality}'

    def __getitem__(self, field):
        return self.__dict__[field]


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