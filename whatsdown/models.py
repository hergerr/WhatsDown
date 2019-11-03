from whatsdown import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import date, datetime


# czy 'data' to to samo co "data"?
# w szczególności przy oznaczaniu rodziców i dzieci w kluczach obcych ('parent) vs ("parent")


class Administrator(db.Model, UserMixin):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return 'Administrator %d, login %s' % (format(self.id), format(self.login))


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
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    # bidirectional relationships
    funerals = relationship("Funeral", back_populates="funeral_home")

    def __repr__(self):
        return 'Dom pogrzebowy {}'.format(self.name)


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
        return 'Nagrobek marki %s, model %s' % (format(self.manufacturer), format(self.material))


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
        return 'Kwatera na cmentarzu nr %d, x %d, y %d' % (self.cemetery_id, self.x_coord, self.y_coord)


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
        return 'Cmentarz w woj. %s, powiat %s, miejscowość %s, ulica %s ' % (
            format(self.voivodeship), format(self.county), format(self.locality), format(self.street))


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
        return '%s, marki  %s, rozmiar %s, w kolorze %s' % (
            format(self.type_of_clothing), format(self.brand), format(self.size), format(self.color))


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
        return 'Pojemnik %s, wykonany z %s' % (format(self.manufacturer), format(self.material))


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
        return 'Pochowany %s %s' % (format(self.first_name), format(self.last_name))


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
        return 'Pogrzeb nr {}'.format(self.id)

    # table many-to-many
    priest_temple = db.Table('priest_temple',
                             db.Column('priest_id', db.Integer(), db.ForeignKey('priest.id'), primary_key=True),
                             db.Column('temple_id', db.Integer(), db.ForeignKey('temple.id'), primary_key=True))


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
        return 'Kapłan {}, {}' % (format(self.first_name), format(self.last_name))


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
        return 'Swiątynia wyznania {}, umiejscowiona w {}, {}, {}' % (
            format(self.religion), format(self.voivodeship), format(self.county), format(self.locality))
