from pyramid.config import Configurator
from pyramid.session import BaseCookieSessionFactory

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

import zope.sqlalchemy

def get_session_factory(engine):
    """Return a generator of database session objects."""
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager):
    """Build a session and register it as a transaction-managed session."""
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    my_session_factory = BaseCookieSessionFactory('itsaseekreet')
    with Configurator(settings=settings, session_factory=my_session_factory) as config:
        settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

        config.include('pyramid_jinja2')
        config.include('pyramid_bootstrap')
        config.include('pyramid_sqlalchemy')
        config.include('pyramid_tm')
        config.include('.routes')

        session_factory = get_session_factory(engine_from_config(settings, prefix='sqlalchemy.'))
        config.registry['dbsession_factory'] = session_factory
        
        config.add_request_method(
            lambda request: get_tm_session(session_factory, request.tm),
            'dbsession',
            reify=True
        )
        config.scan()
    return config.make_wsgi_app()