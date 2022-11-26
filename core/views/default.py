from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from ..forms import RegistrationForm, TrainForm
from ..models import User, Trains

from datetime import datetime, timedelta

@view_config(route_name='home')
# @view_config(route_name='home', request_method="GET", renderer='json')
def index(request):
    print(request.dbsession.query(User).all())
    print(request.dbsession.query(Trains).all())
    # print(len(request.dbsession.query(User).all()))
    if not request.authenticated_userid:
        url = request.route_url('login') 
        return HTTPFound(location=url)


    all_trains = request.dbsession.query(Trains).all()
    return render_to_response('templates/viewtrains.jinja2', {'page_title': 'Home', 'all_trains': all_trains}, request=request)

@view_config(route_name='register')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        username    = form.username.data
        password    = form.password.data
        name        = form.name.data
        email       = form.email.data
        phone       = form.phone.data
        
        new_user = User(username=username, password=password, name=name, email=email, phone=phone, is_active=True, ip_address=request.remote_addr)
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return render_to_response('templates/register.jinja2', {'form': form, 'page_title': 'Register'}, request=request)

@view_config(route_name='addTrain')
def addTrain(request):
    form = TrainForm(request.POST)
    if request.method == 'POST' and form.validate():
        train_number        = form.train_number.data
        train_name          = form.train_name.data
        source              = form.source.data
        destination         = form.destination.data
        time_               = form.time.data
        price               = form.price.data
        seats_available     = form.seats_available.data
        
        str_time = f'{str(datetime.now().year)}-{str(datetime.now().month)}-{str(datetime.now().day)} {str(time_.hour)}:{str(time_.minute)}:00'
        train_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        
        new_train = Trains(train_number=train_number, train_name=train_name, source=source, time=train_time, destination=destination, price=price, 
                            seats_available=seats_available,
                     ip_address=request.remote_addr)
        request.dbsession.add(new_train)
        return HTTPFound(location=request.route_url('addTrain'))
    return render_to_response('templates/addtrain.jinja2', {'form': form, 'page_title': 'Add Train'}, request=request)