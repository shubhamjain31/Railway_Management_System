from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField
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