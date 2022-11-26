from pyramid.httpexceptions import HTTPFound

def login_required(wrapped):
    def wrapper(request, *args, **kw):
        user=request.authenticated_userid
        print(user) 
        if user is None:
            url = request.route_url('login') 
            return HTTPFound(location=url)
        else:
            return wrapped(request, *args, **kw)
    return wrapper