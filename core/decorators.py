from pyramid.httpexceptions import HTTPFound

def login_required(wrapped):
    def wrapper(request, *args, **kw):
        user = request.authenticated_userid
        
        if user is None:
            url = request.route_url('login') 
            return HTTPFound(location=url)
        else:
            return wrapped(request, *args, **kw)
    return wrapper

def is_authenticate(wrapped):
    def wrapper(request, *args, **kw):
        user_session = bool(request.session)

        if user_session is False:
            url = request.route_url('logout') 
            return HTTPFound(location=url)
        else:
            return wrapped(request, *args, **kw)
    return wrapper