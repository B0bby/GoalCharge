from wtforms import Form, TextField, PasswordField, validators
from flask.ext.mongoengine.wtf import model_form
from GoalCharge.models import User

LoginForm = model_form(User,
        exclude=['email','display_name','register_date','charge','is_admin'])

RegisterForm = model_form(User)

#def LoginForm(Form):
#    username = TextField("Username", [validators.Required()])
#    password = PasswordField("Password", [validators.Required()])

#def RegisterForm(Form):
#    username = TextField("Username", [validators.Required(), validators.Length(min=2, max=30)])
#    email = TextField("Email", [validators.Required()])
#    password = PasswordField("Password", [validators.Required(), validators.EqualTo('password_confirm', message='Passwords must match')])
#    password_confirm = PasswordField("Confirm Password", [validators.Required()])

