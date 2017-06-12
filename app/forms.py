from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, DateField, DateTimeField, SelectField, HiddenField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Required, Optional, Email, Regexp, ValidationError
from flask import flash

from app.users import select_user_by_name

#taalla maaritellaan kaikki formit ja niiden validaatio

#metodi jotta voidaan todeta etta jos joku on TRUE niin jokin on pakollinen (kaytetaan esim. notejen ajassa)
class RequiredIf(Required):
    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data:
            super(RequiredIf, self).__call__(form, field)

# class Unique_name(object):
#     #Unique validator
#
#     def __init__(self, message=None):
#         if not message:
#             message = u'this user already exists'
#             self.message = message
#
#     def __call__(self, form, field):
#         usernameField = form._fields.get('username')
#         check = select_user_by_name(usernameField.data)
#         if check is not None:
#             raise ValidationError(self.message)

#nayttaa kaikki errorit jos validointi epaonnistuu
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

class UserCreateForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=35, message="Username length should be between 4 and 35 and it should only contain letters and numbers."), Regexp('^\w+$', message="Username should contain only letters and numbers")])
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=35), Email("Requires valid email address.")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, message="Password too short, minimum length is 6 digits."), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('confirm', validators=[DataRequired()])

class UserEditForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=35)])
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=35), Email()])
    confirm = PasswordField('confirm', validators=[DataRequired()])

class UserPasswordEditForm(Form):
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, message="Password too short, minimum length is 6 digits."),Regexp('^\w+$', message="Username should contain only letters and numbers"),
                                                     EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('confirm', validators=[DataRequired()])
    oldPassword = PasswordField('password', validators=[DataRequired()])

class NoteEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    isTimed = BooleanField('isTimed', default=False)
    time = TimeField('time', validators=[Optional(), RequiredIf('isTimed')])

class TodoAddForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    focus = SelectField('focus', coerce=int)

class TodoEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    focus = SelectField('focus', coerce=int)
    completeStatus = BooleanField('completeStatus', validators=[Optional(), RequiredIf('isTimed')])

class GoalAddForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    end_date = DateTimeField('end_date', validators=[Optional()])

class FocusAddForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])

class GoalEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    end_date = DateField('end_date', validators=[Optional()])
    isActive = BooleanField('isActive')

class FocusEditForm(Form):
    text = StringField('text', validators=[DataRequired(message="Enter text")])
    isActive = BooleanField('isActive')

class GroupAddForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])

class DiscussionAddForm(Form):
    title = StringField('title', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])

class AffirmationForm(Form):
    text = StringField('text', validators=[DataRequired()])
    date = HiddenField('date', validators=[Optional()])

class AffirmationEditForm(Form):
    text = StringField('text', validators=[DataRequired()])