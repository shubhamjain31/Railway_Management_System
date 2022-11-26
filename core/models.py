import cryptacular.bcrypt

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    DateTime,
    Boolean
    )

from sqlalchemy.orm import relationship, synonym

from sqlalchemy.types import (
    Integer,
    Unicode,
    UnicodeText,
    String,
    Float,
    Text
    )

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
# from webhelpers2.text import urlify 
from slugify import slugify

from datetime import datetime
import secrets

Base = declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
    return crypt.encode(password)


class User(Base):
    """
    Application's user model.
    """
    __tablename__ = 'users'

    user_id         = Column(Integer, primary_key=True)
    username        = Column(String(16), nullable=False)
    name            = Column(Unicode(50))
    email           = Column(Unicode(50))
    token           = Column(Unicode, nullable=False)
    phone           = Column(String(16), nullable=False)
    is_superuser    = Column(Boolean, unique=False, default=False)
    is_active       = Column(Boolean, unique=False, default=True)
    is_staff        = Column(Boolean, unique=False, default=False)
    is_verified     = Column(Boolean, unique=False, default=False)
    date_joined     = Column(DateTime, nullable=False)
    ip_address      = Column(String(50), nullable=False)
    browser_info    = Column(Text, nullable=True)

    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, *args, **kwargs):
        if kwargs['username'] == "admin":
            self.is_superuser = True
            
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = secrets.token_urlsafe(64)

class Trains(Base):
    """
    Application's train model.
    """
    __tablename__ = 'trains'

    train_id            = Column(Integer, primary_key=True)
    train_number        = Column(String(50), nullable=False)
    train_name          = Column(String(50), nullable=False)
    source              = Column(Unicode(150))
    destination         = Column(Unicode(150))
    price               = Column(Float)
    seats_available     = Column(Integer, nullable=False)
    time                = Column(DateTime, nullable=False)
    ip_address          = Column(String(50), nullable=False)
    browser_info        = Column(Text, nullable=True)

    @property
    def slug(self):
        return slugify(self.train_number)

class Persons(Base):
    """
    Application's person model.
    """
    __tablename__ = 'persons'

    person_id                   = Column(Integer, ForeignKey('trains.train_id', ondelete='CASCADE'), primary_key=True)
    name                        = Column(String(50), nullable=False)
    age                         = Column(Integer, nullable=False)
    gender                      = Column(Unicode(20))
    email                       = Column(Unicode(150))
    date_and_time_of_booking    = Column(DateTime, default=datetime.utcnow)
    train                       = relationship('Trains', backref='persons')
    ip_address                  = Column(String(50), nullable=False)
    browser_info                = Column(Text, nullable=True)