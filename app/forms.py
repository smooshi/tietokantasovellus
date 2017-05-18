from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    uname = StringField('uname', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)