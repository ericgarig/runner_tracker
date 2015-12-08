from app import db, bcrypt
from sqlalchemy.sql import collate


class Athlete(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_first = db.Column(db.String(64), index=True)
	name_last = db.Column(db.String(64), index=True)
	phone_number = db.Column(db.String(10), index=True)
	ice_name = db.Column(db.String(64), index=True)
	ice_phone = db.Column(db.String(10), index=True)
	workouts = db.relationship('Workout', backref='athlete', lazy='dynamic')
	note = db.Column(db.Text, index=True)
	date_birth = db.Column(db.Date, index=True)
	email = db.Column(db.String(64), index=True)
	disability = db.Column(db.String(64), index=True)
	pace = db.Column(db.Float, index=True)
	address_street = db.Column(db.String(64), index=True)
	address_city = db.Column(db.String(64), index=True)
	address_state = db.Column(db.String(2), index=True)
	address_zip = db.Column(db.String(5), index=True)
	is_handcrank = db.Boolean()

	def __repr__(self):
		return '<Athlete %r %r>' % (self.name_first, self.name_last)

	def name_fl(self):
		return '%s %s' % (self.name_first, self.name_last)

	def name_lf(self):
		return '%s, %s' % (self.name_last, self.name_first)

	def phone_display(self):
		if len(self.phone_number) == 10:
			return '(%s) %s-%s' % (self.phone_number[:3], self.phone_number[3:6], self.phone_number[6:] )

	def ice_phone_display(self):
		if len(self.ice_phone) == 10:
			return '(%s) %s-%s' % (self.ice_phone[:3], self.ice_phone[3:6], self.ice_phone[6:] )

	def address_string(self):
		if (self.address_street == None and 
				self.address_city == None and 
				self.address_state == None and 
				self.address_zip == None):
			return None
		else:
			return '%s, %s, %s %s' % (
				self.address_street if self.address_street != None else 'Unknown Street', 
				self.address_city if self.address_city != None else 'Unknown City', 
				self.address_state if self.address_state != None else 'Unknown State', 
				self.address_zip if self.address_zip != None else 'Unknown Zip'
				)


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

	def pace_avg(self):
		workouts = Workout.query.join(
			Athlete,Workout.athlete_id == Athlete.id).filter(
			Athlete.id == self.id).filter(
			Workout.speed != None ).filter(
			Workout.distance != None )
		return round(
			(sum(one_workout.duration() for one_workout in workouts))/
			(sum(one_workout.distance for one_workout in workouts))
			,2) if workouts.first() != None else 0



class Workout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))
	date = db.Column(db.Date, index=True)
	distance = db.Column(db.Float, index=True)
	speed = db.Column(db.Float, index=True)
	note = db.Column(db.Text, index=True)

	def __repr__(self):
		return '<Workout %r>' % (self.athlete_id)

	def athlete_name(self):
		return Athlete.query.get(self.athlete_id).name_fl()

	def date_display(self):
		return self.date.strftime("%a, %m/%d/%y")

	def display_distance(self):
		return self.distance if self.distance != None else None

	def display_speed(self):
		return self.speed if self.speed != None else None

	def duration(self):
		return (self.distance * self.speed 
			if self.distance != None and self.speed != None 
			else None)



class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self):
		self.name = name
		self.password = bcrypt.generate_password_hash(password)

	def __repr__(self):
		return '<User %r>' % (self.name)