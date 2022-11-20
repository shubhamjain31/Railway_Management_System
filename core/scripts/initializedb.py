from sqlalchemy import engine_from_config
from decouple import config
from core.models import Base

def main():
    settings = {'sqlalchemy.url': config("SQLALCHEMY_URL")}
    engine = engine_from_config(settings, prefix='sqlalchemy.')

    if bool(config("DEBUG", '')):
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)