from wtforms import Form, TextField, PasswordField, validators

def LoginForm(Form):
    username = TextField("Username", [validators.Required()])
    password = PasswordField("Password", [validators.Required()])

def RegisterForm(Form):
    username = TextField("Username", [validators.Required(), validators.Length(min=2, max=30)])
    email = TextField("Email", [validators.Required()])
    password = PasswordField("Password", [validators.Required(), validators.EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField("Confirm Password", [validators.Required()])

