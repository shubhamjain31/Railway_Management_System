from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, FloatField, TimeField
from wtforms.validators import InputRequired, Email, Length

strip_filter = lambda x: x.strip() if x else None

class RegistrationForm(Form):
    username    = StringField('Username', [Length(min=1, max=255)], filters=[strip_filter], render_kw={"placeholder": "Username"})
    name        = StringField('Name', [InputRequired("Please enter your name.")], render_kw={"placeholder": "Name"})
    email       = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")], render_kw={"placeholder": "Email"})
    phone       = StringField('Phone Number', [InputRequired("Please enter your phone number.")], render_kw={"placeholder": "Phone Number"})
    password    = PasswordField('Password', [Length(min=8)], render_kw={"placeholder": "Password"})

class LoginForm(Form):
    username    = StringField('Username', [Length(min=1, max=255)], filters=[strip_filter], render_kw={"placeholder": "Username"})
    password    = PasswordField('Password', [Length(min=8)], render_kw={"placeholder": "Password"})

class TrainForm(Form):
    train_number        = StringField('Train Number', [InputRequired("Please enter train number.")], filters=[strip_filter], render_kw={"placeholder": "Train Number"})
    train_name          = StringField('Train Name', [InputRequired("Please enter train name.")], filters=[strip_filter], render_kw={"placeholder": "Train Name"})
    source              = StringField('Source', [InputRequired("Please enter your source.")], render_kw={"placeholder": "Source"})
    destination         = StringField('Destination', [InputRequired("Please enter your destination.")], render_kw={"placeholder": "Destination"})
    time                = TimeField('Time', [InputRequired("Please enter seats availability.")], render_kw={"placeholder": "Time"})
    price               = FloatField('Price', [InputRequired("Please enter price.")], render_kw={"placeholder": "Price"})
    seats_available     = IntegerField('Seats Available', [InputRequired("Please enter seats available.")], render_kw={"placeholder": "Seats Available"})