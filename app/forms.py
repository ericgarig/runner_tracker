from flask.ext.wtf import Form
from wtforms import BooleanField, DateField, DecimalField, HiddenField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NoneOf, NumberRange, Optional
from app.models import Athlete


class EditForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	name_first = StringField('name_first', validators=[DataRequired()])
	name_last = StringField('name_last', validators=[DataRequired()])
	phone_number = StringField('phone_number')
	email = StringField('email', validators=[Email(message='Not a valid email address')])
	address_street = StringField('address_street')
	address_city = StringField('address_city')
	address_state = StringField('address_state', validators=[Length(max=2)])
	address_zip = StringField('address_zip')
	date_birth = DateField('date_birth')
	disability = StringField('disability')
	pace = DecimalField('pace')
	ice_name = StringField('ice_name')
	ice_phone = StringField('ice_phone')
	note = TextAreaField('note')
	is_handcrank = BooleanField('is_handcrank')


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
	