from pyramid.config import Configurator
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import BaseCookieSessionFactory

from sqlalchemy import engine_from_config

from core.model import (
    DBSession,
    RootFactory,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    session_factory = BaseCookieSessionFactory(
        settings['session.secret']
        )

    authn_policy = SessionAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()

    with Configurator(settings=settings, root_factory=RootFactory, authentication_policy=authn_policy, authorization_policy=authz_policy, session_factory=session_factory) as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_bootstrap')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()