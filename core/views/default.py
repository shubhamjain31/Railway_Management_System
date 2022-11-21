from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from ..forms import RegistrationForm, LoginForm
from ..models import User

@view_config(route_name='home')
# @view_config(route_name='home', request_method="GET", renderer='json')
def index(request):
    print(len(request.dbsession.query(User).all()))
    if not request.authenticated_userid:
        url = request.route_url('login') 
        return HTTPFound(location=url)
    
    form = LoginForm()
    # print(request.authenticated_userid)
    return render_to_response('templates/index.jinja2', {'form': form, 'page_title': 'Home'}, request=request)

@view_config(route_name='register')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        username    = form.username.data
        password    = form.password.data
        name        = form.name.data
        email       = form.email.data
        phone       = form.phone.data
        
        new_user = User(username=username, password=password, name=name, email=email, phone=phone)
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return render_to_response('templates/register.jinja2', {'form': form, 'page_title': 'Register'}, request=request)