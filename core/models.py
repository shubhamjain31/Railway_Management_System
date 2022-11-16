import cryptacular.bcrypt

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    DateTime,
    )

from sqlalchemy.orm import relationship, synonym

from sqlalchemy.types import (
    Integer,
    Unicode,
    UnicodeText,
    String,
    )

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


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
    date_joined     = Column(DateTime, nullable=False)

    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = secrets.token_urlsafe(64)

    # @classmethod
    # def get_by_username(cls, username):
    #     return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return crypt.check(user.password, password)