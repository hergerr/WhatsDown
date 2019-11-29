from whatsdown import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session
from sqlalchemy import ForeignKey, event
from datetime import date, datetime
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool


class Administrator(db.Model, UserMixin):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Administrator {self.id}, login {self.login}'


class FuneralHome(db.Model, UserMixin):
    # connected with funeral o-t-m
    # atributes
    __tablename__ = 'funeral_home'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(30), unique=True)
    voivodeship = db.Column(db.Text)
    county = db.Column(db.Text)
    locality = db.Column(db.Text)
    phone = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)

    # relationships
    funerals = relationship("Funeral", back_populates="funeral_home")

    def __repr__(self):
        return f'Dom pogrzebowy {self.name}'


class Tombstone(db.Model):  # connected with quarter o-t-m
    # atributes
    __tablename__ = 'tombstone'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    manufacturer = db.Column(db.Text)
    material = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __repr__(self):
        return f'Nagrobek marki {self.manufacturer}, model {self.material}'


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
    cemetery = relationship("Cemetery", back_populates="quarters",  single_parent=True)
    buried = relationship("Buried", back_populates="quarter", cascade="save-update, merge, delete")
    tombstone = relationship("Tombstone")

    def __repr__(self):
        return f'Kwatera na cmentarzu nr {self.cemetery_id}, x={self.x_coord}, y={self.y_coord}'


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

    # relationships
    quarters = relationship("Quarter", back_populates="cemetery", cascade="save-update, merge, delete")

    def __repr__(self):
        return f'Cmentarz w woj. {self.voivodeship}, powiat {self.county}, miejscowość {self.locality}, ulica {self.street}'


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

    def __repr__(self):
        return f'{self.type_of_clothing}, marki  {self.brand}, rozmiar {self.size}, w kolorze {self.color}'


class Container(db.Model):
    # connected with buried m-t-o

    # atributes
    __tablename__ = 'container'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type_of_container = db.Column(db.Text)
    manufacturer = db.Column(db.Text)
    material = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __repr__(self):
        return f'Pojemnik {self.manufacturer}, wykonany z {self.material}'


class Buried(db.Model):
    # connected with outfit o-t-m
    # connected with container o-t-m
    # connected with quarter o-t-m

    # atributes
    __tablename__ = 'buried'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.Date())
    death_date = db.Column(db.Date())
    cause_of_death = db.Column(db.Text)

    # foreign keys
    outfit_id = db.Column(db.Integer, ForeignKey('outfit.id'), nullable=False)
    container_id = db.Column(db.Integer, ForeignKey('container.id'), nullable=False)
    quarter_id = db.Column(db.Integer, ForeignKey('quarter.id'), nullable=False)
    funeral_id = db.Column(db.Integer, ForeignKey('funeral.id'), nullable=False)

    # relationships
    quarter = relationship("Quarter", back_populates="buried", single_parent=True)
    funeral = relationship("Funeral", back_populates="buried", single_parent=True, cascade="all, delete-orphan",
                           passive_deletes=True)
    container = relationship("Container")
    outfit = relationship("Outfit")

    def __repr__(self):
        return f'Pochowany {self.first_name} {self.last_name}'


class Funeral(db.Model):
    # connected with funeral_home o-t-m
    # connected with buried m-t-o
    # connected with (priest&temple) o-t-m

    # atributes
    __tablename__ = 'funeral'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.Date(), default=datetime.now(), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    # foreign keys
    funeral_home_id = db.Column(db.Integer, ForeignKey('funeral_home.id'), nullable=True)
    priest_temple_id = db.Column(db.Integer, ForeignKey('priest_temple.id'), nullable=False)

    # relationships
    buried = relationship("Buried", back_populates="funeral", cascade="save-update, merge, delete")
    funeral_home = relationship("FuneralHome", back_populates="funerals")
    priest_temple = relationship("PriestTemple", single_parent=True)

    def __repr__(self):
        return f'Pogrzeb nr {self.id}'


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

    # relationship
    temples = relationship('Temple', secondary="priest_temple")

    def __repr__(self):
        return f'Kapłan {self.first_name}, {self.last_name}'


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

    # relationship
    priests = relationship('Priest', secondary="priest_temple")

    def __repr__(self):
        return f'Swiątynia wyznania {self.religion}, umiejscowiona w {self.voivodeship}, {self.county}, {self.locality}'


class PriestTemple(db.Model):
    __tablename__ = 'priest_temple'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    priest_id = db.Column('priest_id', db.Integer(), db.ForeignKey('priest.id'))
    temple_id = db.Column('temple_id', db.Integer(), db.ForeignKey('temple.id'))

    # relationship
    priest = relationship("Priest", backref=db.backref("temple_association", cascade="all, delete-orphan"),
                          passive_deletes=True)
    temple = relationship("Temple", backref=db.backref("priest_association", cascade="all, delete-orphan"),
                          passive_deletes=True)

    def __repr__(self):
        return f'Kapłan {self.priest_id}, Świątynia {self.temple_id}'


# usuwanie pogrzebu bez pochowanych
@event.listens_for(Buried, 'before_delete')
def delete_reference(mapper, connection, target):
    # after_flush used for consistent results
    @event.listens_for(Session, 'after_flush', once=True)
    def receive_after_flush(session, context):
        # if this buried was last in funeral
        if target.funeral and not target.funeral.buried:
            session.delete(target.funeral)
