from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

import zope.sqlalchemy

from .security import CookieCSRFStoragePolicy, SecurityPolicy

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

    my_session_factory = SignedCookieSessionFactory('seekrit', timeout=None)
    config = Configurator(settings=settings, session_factory=my_session_factory)
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    config.include('pyramid_jinja2')
    config.include('pyramid_bootstrap')
    config.include('pyramid_sqlalchemy')
    config.include('pyramid_tm')
    config.include('.routes')

    config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
    config.set_default_csrf_options(require_csrf=True)

    config.set_security_policy(SecurityPolicy(secret=settings['core.secret']))


    session_factory = get_session_factory(engine_from_config(settings, prefix='sqlalchemy.'))
    config.registry['dbsession_factory'] = session_factory
    
    config.add_request_method(
        lambda request: get_tm_session(session_factory, request.tm),
        'dbsession',
        reify=True
    )
    config.scan()

    app = config.make_wsgi_app()
    return app