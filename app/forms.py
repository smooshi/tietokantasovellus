from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo
from flask import flash

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class UserCreateForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=35)])
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=35)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, message="Password too short"), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('confirm')

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

class UserEditForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=35)])
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=35)])
#    password = PasswordField('password', validators=[])
    confirm = PasswordField('confirm', validators=[DataRequired(message="Enter current password to confirm changes")])

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

class NoteEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    #date = DateTimeField('date', validators=[DataRequired()])