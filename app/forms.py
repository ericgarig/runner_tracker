from decimal import Decimal, ROUND_UP
from flask.ext.wtf import Form
from wtforms import BooleanField, DateField, DecimalField, HiddenField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NoneOf, NumberRange, Optional
from app.models import Athlete


class EditForm(Form):
    id = HiddenField('id', validators=[DataRequired(message='Internal ID undefined')])
    name_first = StringField('First Name', validators=[DataRequired(message='Must enter a first name')])
    name_last = StringField('Last Name', validators=[DataRequired(message='Must enter a last name')])
    phone_number = StringField('Phone Number', validators=[Optional()], default = '')
    email = StringField('Email', validators=[Optional(), Email(message='Not a valid email address')], default = '')
    date = DateField('Date of Birth', validators=[Optional()])
    address_street = StringField('Street', validators=[Optional()], default = '')
    address_city = StringField('City', validators=[Optional()], default = '')
    address_state = StringField('State', validators=[Optional(), Length(max=2, message='State must be 2 letters')], default = '')
    address_zip = StringField('Zip', validators=[Optional()], default = '')
    ice_name = StringField('Emergency Name', validators=[Optional()], default = '')
    ice_phone = StringField('Emergency Phone', validators=[Optional()], default = '')
    ice_email = StringField('Emergency Email', validators=[Optional()], default = '')
    pace = StringField('Pace ( min/mile )', validators=[Optional()])
    disability = StringField('Disability', validators=[Optional()], default = '')
    note = TextAreaField('Note', validators=[Optional()], default = '')
    is_handcrank = BooleanField('Handcrank?', validators=[Optional()], default=0)


class DeleteForm(Form):
    id = HiddenField('id', validators=[DataRequired(message='Internal ID undefined')])
    name_first = StringField('name_first', validators=[DataRequired(message='Must enter a first name')])
    name_last = StringField('name_last', validators=[DataRequired(message='Must enter a last name')])


class WorkoutForm(Form):
    id = HiddenField('id', validators=[DataRequired(message='Internal ID undefined')])
    date = DateField('date', validators=[DataRequired(message='Date must be specified')])
    distance = DecimalField('distance', validators=[Optional(), NumberRange(min=0.1, message='Distance must be a number value greater than 0.1')])
    speed = DecimalField('speed', validators=[Optional(), NumberRange(min=0.1, message='Speed must be a number value greater than 0.1')])
    note = TextAreaField('note')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message='Username cannot be blank')])
    password = PasswordField('password', validators=[DataRequired(message='Password cannot be blank')])
    
