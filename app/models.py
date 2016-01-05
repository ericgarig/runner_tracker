from app import db, bcrypt
from sqlalchemy.sql import collate


class Athlete(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_first = db.Column(db.String(64), index=True)
	name_last = db.Column(db.String(64), index=True)
	phone_number = db.Column(db.String(10), index=True)
	email = db.Column(db.String(64), index=True)
	date_birth = db.Column(db.Date, index=True)
	address_street = db.Column(db.String(64), index=True)
	address_city = db.Column(db.String(64), index=True)
	address_state = db.Column(db.String(2), index=True)
	address_zip = db.Column(db.String(5), index=True)
	ice_name = db.Column(db.String(64), index=True)
	ice_phone = db.Column(db.String(10), index=True)
	ice_email = db.Column(db.String(64), index=True)
	disability = db.Column(db.String(64), index=True)
	pace = db.Column(db.String(64), index=True)
	shirt_size = db.Column(db.String(5), index=True)
	note = db.Column(db.Text, index=True)
	is_handcrank = db.Column(db.Boolean, index=True)
	workouts = db.relationship('Workout', backref='athlete', lazy='dynamic')

	def __init__(self, name_first, name_last, phone_number=None, email=None, date_birth=None, 
		address_street=None, address_city=None, address_state=None, address_zip=None, 
		ice_name=None, ice_phone=None, ice_email=None, disability=None, pace=None, 
		shirt_size=None, note=None, is_handcrank=0):
		self.name_first = name_first
		self.name_last = name_last
		self.phone_number = phone_number
		self.email = email
		self.date_birth = date_birth
		self.address_street = address_street
		self.address_city = address_city
		self.address_state = address_state
		self.address_zip = address_zip
		self.ice_name = ice_name
		self.ice_phone = ice_phone
		self.ice_email = ice_email
		self.disability = disability
		self.pace = pace
		self.shirt_size = shirt_size
		self.note = note
		self.is_handcrank = is_handcrank

	def __repr__(self):
		return '<Athlete - %r %r>' % (self.name_first, self.name_last)

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
		if (not self.address_street and 
				not self.address_city and 
				not self.address_state and 
				not self.address_zip
				):
			return None
		else:
			return '%s, %s, %s %s' % (
				self.address_street if self.address_street else 'Unknown Street', 
				self.address_city if self.address_city else 'Unknown City', 
				self.address_state if self.address_state else 'unknown-state', 
				self.address_zip if self.address_zip else 'unknown-zip'
				)

	def list_athletes(self):
		return Athlete.query.filter(
			Athlete.is_handcrank != True).order_by(
			collate(Athlete.name_first, 'NOCASE'), 
			collate(Athlete.name_last, 'NOCASE')
			).all()

	def list_crankers(self):
		return Athlete.query.filter(
			Athlete.is_handcrank == True).order_by(
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
		if workouts.first() != None:
			return round((sum(one_workout.duration() for one_workout in workouts))/(sum(one_workout.distance for one_workout in workouts)),2)
		return None



class Workout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))
	date = db.Column(db.Date, index=True)
	distance = db.Column(db.Float, index=True)
	speed = db.Column(db.Float, index=True)
	note = db.Column(db.Text, index=True)

	def __init__(self, athlete_id, date, distance=None, speed=None, note=None):
		self.athlete_id = athlete_id
		self.date = date
		self.distance = distance
		self.speed = speed
		self.note = note

	def __repr__(self):
		return '<Workout - %r>' % (self.athlete_id)

	def athlete_name(self):
		return Athlete.query.get(self.athlete_id).name_fl()

	def date_display(self):
		return self.date.strftime("%a, %m/%d/%y")

	def display_distance(self):
		return self.distance if self.distance else None

	def display_speed(self):
		return self.speed if self.speed else None

	def duration(self):
		return (self.distance * self.speed if self.distance and self.speed else None)



class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	password = db.Column(db.String, nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = bcrypt.generate_password_hash(password)

	def __repr__(self):
		return '<User - %r>' % (self.username)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False
	
	def get_id(self):
	    return unicode(self.id)

