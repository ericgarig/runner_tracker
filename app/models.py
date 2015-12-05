from app import db
from sqlalchemy.sql import collate


class Athlete(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_first = db.Column(db.String(64), index=True)
	name_last = db.Column(db.String(64), index=True)
	nickname = db.Column(db.String(64))
	phone_number = db.Column(db.String(10), index=True)
	ice_name = db.Column(db.String(64), index=True)
	ice_phone = db.Column(db.String(10), index=True)
	workouts = db.relationship('Workout', backref='athlete', lazy='dynamic')

	def name_fl(self):
		return '%s %s' % (self.name_first, self.name_last)

	def phone_display(self):
		if len(self.phone_number) == 10:
			return '(%s) %s-%s' % (self.phone_number[:3], self.phone_number[3:6], self.phone_number[6:] )

	def ice_phone_display(self):
		if len(self.ice_phone) == 10:
			return '(%s) %s-%s' % (self.ice_phone[:3], self.ice_phone[3:6], self.ice_phone[6:] )


	def list_athletes(self):
		return Athlete.query.order_by(
			collate(Athlete.name_first, 'NOCASE'), 
			collate(Athlete.name_last, 'NOCASE')
			).all()

	def workouts(self):
		return Workout.query.join(
			Athlete, 
			(Workout.athlete_id == Athlete.id)
			).filter(Athlete.id==self.id).order_by(Workout.date.desc())

	def __repr__(self):
		return '<Athlete %r %r>' % (self.name_first, self.name_last)


class Workout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))
	date = db.Column(db.Date, index=True)
	distance = db.Column(db.Float, index=True)
	speed = db.Column(db.Float, index=True)

	def athlete_name(self):
		return Athlete.query.get(self.athlete_id).name_fl()

	def date_display(self):
		return self.date.strftime("%a, %m/%d/%y")

	def display_distance(self):
		return self.distance if self.distance != None else '-'

	def display_speed(self):
		return self.speed if self.speed != None else '-'

	def duration(self):
		return self.distance * self.speed if self.distance != None and self.speed != None else '-'

	def __repr__(self):
		return '<Workout %r>' % (self.athlete_id)

