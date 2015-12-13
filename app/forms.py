from decimal import Decimal, ROUND_UP
from flask.ext.wtf import Form
from wtforms import BooleanField, DateField, DecimalField, HiddenField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NoneOf, NumberRange, Optional
from app.models import Athlete


class EditForm(Form):
	id = HiddenField('id', validators=[DataRequired(message='internal ID undefined')])
	name_first = StringField('First Name', validators=[DataRequired(message='must enter a first name')])
	name_last = StringField('Last Name', validators=[DataRequired(message='must enter a last name')])
	phone_number = StringField('Phone Number', validators=[Optional()], default = '')
	email = StringField('Email', validators=[Optional(), Email(message='Not a valid email address')], default = '')
	date = DateField('Date of Birth', validators=[Optional()])
	address_street = StringField('Street', validators=[Optional()], default = '')
	address_city = StringField('City', validators=[Optional()], default = '')
	address_state = StringField('State', validators=[Optional(), Length(max=2, message='must be 2 letters')], default = '')
	address_zip = StringField('Zip', validators=[Optional()], default = '')
	ice_name = StringField('Emergency Name', validators=[Optional()], default = '')
	ice_phone = StringField('Emergency Phone', validators=[Optional()], default = '')
	pace = DecimalField('Pace ( min/mile )', places=2, rounding=ROUND_UP, validators=[Optional()])
	disability = StringField('Disability', validators=[Optional()], default = '')
	note = TextAreaField('Note', validators=[Optional()], default = '')
	is_handcrank = BooleanField('Handcrank?', validators=[Optional()], default=0)


class DeleteForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	name_first = StringField('name_first', validators=[DataRequired()])
	name_last = StringField('name_last', validators=[DataRequired()])


class WorkoutForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])
	distance = DecimalField('distance', validators=[DataRequired(), NumberRange(min=0.1)])
	speed = DecimalField('speed', validators=[DataRequired(), NumberRange(min=0.1)])
	note = TextAreaField('note')


class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	