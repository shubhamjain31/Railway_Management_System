from pyramid.view import view_config
from ..models import User

# @view_config(route_name='home', renderer='core:templates/mytemplate.jinja2')
@view_config(route_name='home', request_method="GET", renderer='json')
def my_view(request):
    # user = User(username="admin", password="demo1234", name="Shubham Jain", email="admin@email.com", phone="9876542310")
    # request.dbsession.add(user)
    print(request.dbsession.query(User).all()[3].password)
    print(request.authenticated_userid)
    return {'project': 'myproject'}