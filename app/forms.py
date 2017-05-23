from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, DateField, DateTimeField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Required, Optional
from flask import flash
from datetime import datetime

class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)

class FlashErrors():
    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

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
    isTimed = BooleanField('isTimed', default=False)
    time = TimeField('time', validators=[Optional(), RequiredIf('isTimed')])

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

class TodoEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])

class GoalAddForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    end_date = DateTimeField('end_date', validators=[Optional()])

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

class GoalEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    end_date = DateTimeField('end_date', validators=[Optional()])
    isActive = BooleanField('isActive')

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))