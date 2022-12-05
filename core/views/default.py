from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from ..forms import RegistrationForm, TrainForm
from ..models import User, Trains, Persons

from datetime import datetime
from core.decorators import login_required

@view_config(route_name='home')
# @view_config(route_name='home', request_method="GET", renderer='json')
def index(request):
    # print(len(request.dbsession.query(Persons).all()))
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
@login_required
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

@view_config(route_name='train')
@login_required
def train(request):
    slug    = request.matchdict['slug']

    all_trains = request.dbsession.query(Trains)
    if request.session['is_superuser'] is not True:
        return render_to_response('templates/viewtrains.jinja2', {'msg': "Not an Admin", 'page_title': 'Home', 'all_trains': all_trains.all()}, request=request)

    train_obj = all_trains.filter_by(train_number=slug).first()
    persons = request.dbsession.query(Persons).join(Trains).filter(Trains.train_number == slug).all()
    return render_to_response('templates/viewperson.jinja2', {'train': train_obj, 'persons': list(persons), 'page_title': 'Edit Train'}, request=request)

temp = {}
@view_config(route_name='book')  
@login_required
def book(request):
    global temp
    source          = request.POST.get('source')
    destination     = request.POST.get('destination')
    name            = request.POST.get('name')
    age             = request.POST.get('age')
    gender          = request.POST.get('gender')
    if request.authenticated_userid:
        trains = request.dbsession.query(Trains).filter_by(source=source.replace("_", " "), destination=destination.replace("_", " "))

        if trains.count():
            temp['name']        = name
            temp['age']         = age
            temp['gender']      = gender

            return render_to_response('templates/trainsavailable.jinja2', {'trains': trains, 'page_title': 'Available Trains' }, request=request)
        else:
            message_data = "Not Found"
            return render_to_response('templates/404.jinja2', {'message_data': message_data, 'page_title': 'Error Page'}, request=request)

    else:
        message_data = "Not a valid user. Please Login to continue"
        return render_to_response('templates/404.jinja2', {'message_data': message_data, 'page_title': 'Error Page'}, request=request)

@view_config(route_name='booking')  
@login_required
def booking(request):
    slug    = request.matchdict['slug']

    train_obj = request.dbsession.query(Trains)
    train_obj = train_obj.filter_by(train_number=slug).first()

    if train_obj.seats_available == 0:
        return render_to_response('templates/viewtrains.jinja2', {'msg': "Not an Admin", 'page_title': 'Home', 'all_trains': train_obj.all()}, request=request)
    train_obj.seats_available -= 1

    new_person = Persons(train=train_obj, name=temp['name'], email=request.session['email'],age=temp['age'],gender=temp['gender'],
                     ip_address=request.remote_addr)
    request.dbsession.add(new_person)
    request.dbsession.add(train_obj)

    message_data = "Booked Successfully...Price to be paid is "+str(train_obj.price)
    return render_to_response('templates/viewperson.jinja2', {'message_data': message_data, 'page_title': 'View Person', 'train':train_obj}, request=request)

@view_config(route_name='bookingform')  
@login_required
def bookingform(request):

    all_trains = request.dbsession.query(Trains).all()

    sources = []; destinations = []

    for i in all_trains:
        sources.append(i.source)
        destinations.append(i.destination)

    sources      = list(set(sources))
    destinations = list(set(destinations))

    if request.authenticated_userid:
        return render_to_response('templates/booking.jinja2', {'sources': sources, 'page_title': 'Bookings', 'destinations': destinations}, request=request)
    else:
        message_data = "User not authenticated"
        return render_to_response('templates/404.jinja2', {'message_data': message_data, 'page_title': 'Error Page'}, request=request)

@view_config(route_name='mybooking')  
@login_required
def mybooking(request):

    if request.authenticated_userid:
        persons = request.dbsession.query(Persons).filter_by(email=request.session['email'])
        return render_to_response('templates/mybooking.jinja2', {'persons': persons, 'page_title': 'My Bookings'}, request=request)
    else:
        message_data = "User not authenticated"
        return render_to_response('templates/404.jinja2', {'message_data': message_data, 'page_title': 'Error Page'}, request=request)

@view_config(route_name='profile')  
@login_required
def profile(request):
    id    = request.matchdict['id']
    person = request.dbsession.query(Persons).filter_by(person_id=id).first()
    return render_to_response('templates/profile.jinja2', {'person': person, 'page_title': 'Profile'}, request=request)