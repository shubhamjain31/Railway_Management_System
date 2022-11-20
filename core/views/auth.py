from pyramid.csrf import new_csrf_token
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.renderers import render_to_response
from pyramid.security import (
    remember,
    forget,
)
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..security import (
    USERS,
    check_password
)

from .. import models
from ..forms import LoginForm


@view_config(route_name='login', renderer='core:templates/login.jinja2')
def login(request):

    message = ''
    username = ''

    form = LoginForm(request.POST)
    if request.method == 'POST':
        username    = form.username.data
        password    = form.password.data
        user = (
            request.dbsession.query(models.User)
            .filter_by(username=username)
            .first()
        )
        if user is not None and check_password(password, user.password):
            new_csrf_token(request)
            headers = remember(request, user.user_id)
            return HTTPSeeOther(location=request.route_url('home'), headers=headers)
        message = 'Failed login'
        request.response.status = 400

    return render_to_response('templates/login.jinja2', {'form': form, 'message': message}, request=request)
    
@view_config(route_name='logout')
def logout(request):
    next_url = request.route_url('home')
    new_csrf_token(request)
    headers = forget(request)
    return HTTPSeeOther(location=next_url, headers=headers)

@forbidden_view_config(renderer='core:templates/403.jinja2')
def forbidden_view(exc, request):
    if not request.is_authenticated:
        next_url = request.route_url('login', _query={'next': request.url})
        return HTTPSeeOther(location=next_url)

    request.response.status = 403
    return {}