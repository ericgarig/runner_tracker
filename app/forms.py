from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, DecimalField, DateField, FloatField
from wtforms.validators import DataRequired, Length, NoneOf, NumberRange
from app.models import Athlete


class EditForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	name_first = StringField('name_first', validators=[DataRequired()])
	name_last = StringField('name_last', validators=[DataRequired()])
	phone_number = StringField('phone_number', validators=[Length(min=0, max=10)])
	ice_phone = StringField('ice_phone', validators=[Length(min=0, max=10)])
	ice_name = StringField('ice_name')


class DeleteForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	name_first = StringField('name_first', validators=[DataRequired()])
	name_last = StringField('name_last', validators=[DataRequired()])


class WorkoutForm(Form):
	id = HiddenField('id', validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])
	distance = DecimalField('distance', validators=[DataRequired(), NumberRange(min=0.1)])
	speed = DecimalField('speed', validators=[DataRequired(), NumberRange(min=0.1)])
