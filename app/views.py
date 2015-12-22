from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import current_user, login_user, logout_user, login_required
from datetime import date
from app import app, bcrypt, db, lm
from .forms import EditForm, DeleteForm, LoginForm, WorkoutForm
from .models import Athlete, Workout, User


# ##########################
# ERRORS
# ##########################
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500


# ##########################
# LOGINS
# ##########################
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = ''
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash('You were logged in.')
			return redirect(url_for('list_athlete'))
		else:
			error = 'Invalid username or password.'
	return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You were logged out.')
	return redirect(url_for('login'))


# ##########################
# ATHLETES
# ##########################

@app.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('list_athlete'))
	return redirect(url_for('login'))


@app.route('/athlete')
@login_required
def list_athlete():
	athletes = Athlete.query.first()
	return render_template('athlete_list.html', athletes=athletes)


@app.route('/athlete/new', methods=['GET', 'POST'])
@login_required
def create_athlete():
	form = EditForm()
	if form.validate_on_submit():
		new = Athlete(
				name_first=form.name_first.data,
				name_last=form.name_last.data,
				phone_number =convert_to_digits(form.phone_number.data),
				email=form.email.data,
				date_birth=date_if_older_than_decade(form.date.data),
				address_street=form.address_street.data,
				address_city=form.address_city.data,
				address_state=form.address_state.data,
				address_zip=form.address_zip.data,
				ice_name=form.ice_name.data,
				ice_phone=convert_to_digits(form.ice_phone.data),
				pace=form.pace.data,
				disability=form.disability.data,
				note=form.note.data,
				is_handcrank=form.is_handcrank.data
				)
		db.session.add(new)
		db.session.commit()
		flash('New athlete created.')
		return redirect(url_for('list_athlete'))
	else:
		form.id.data = 0
	return render_template('athlete_edit.html', form=form)


@app.route('/athlete/<int:id>')
@login_required
def view_athlete(id):
	athlete = Athlete.query.get(id)
	return render_template('athlete.html', athlete=athlete)


@app.route('/athlete/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_athlete(id):
	form = EditForm()
	print form.data
	athlete = Athlete.query.get(id)
	if form.validate_on_submit():
		athlete.name_first = form.name_first.data
		athlete.name_last = form.name_last.data
		athlete.phone_number = convert_to_digits(form.phone_number.data)
		athlete.email = form.email.data
		athlete.date_birth = date_if_older_than_decade(form.date.data)
		athlete.address_street = form.address_street.data
		athlete.address_city = form.address_city.data
		athlete.address_state = form.address_state.data
		athlete.address_zip = form.address_zip.data
		athlete.ice_phone = convert_to_digits(form.ice_phone.data)
		athlete.ice_name = form.ice_name.data
		athlete.pace = form.pace.data
		athlete.disability = form.disability.data
		athlete.note = form.note.data
		athlete.is_handcrank = form.is_handcrank.data
		db.session.commit()
		flash('Athlete info updated.')
		return redirect(url_for('view_athlete', id=athlete.id))
	else:
		form.id.data = id
		form.name_first.data = athlete.name_first
		form.name_last.data = athlete.name_last
		form.phone_number.data = athlete.phone_number
		form.email.data = athlete.email
		form.date.data = athlete.date_birth
		form.address_street.data = athlete.address_street
		form.address_city.data = athlete.address_city
		form.address_state.data = athlete.address_state
		form.address_zip.data = athlete.address_zip
		form.ice_phone.data = athlete.ice_phone
		form.ice_name.data = athlete.ice_name
		form.pace.data = athlete.pace
		form.disability.data = athlete.disability
		form.note.data = athlete.note
		form.is_handcrank.data = athlete.is_handcrank
	return render_template('athlete_edit.html', form=form)


@app.route('/athlete/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_athlete(id):
	form = DeleteForm()
	athlete = Athlete.query.get(id)
	if form.validate_on_submit():
		if form.name_first.data == athlete.name_first and form.name_last.data == athlete.name_last:
			deleted_name = athlete.name_fl()
			db.session.delete(athlete)
			db.session.commit()
			flash('%s  has been removed.' % (deleted_name))
			return redirect(url_for('list_athlete'))
		else:
			form.id.data = id
			flash('Please type in the first and last name to confirm delering of %s.' % (athlete.name_fl()))
	return render_template('athlete_delete.html', form=form, athlete=athlete)


# ##########################
# WORKOUT
# ##########################
@app.route('/workout/<int:id>/new', methods=['GET', 'POST'])
@login_required
def new_workout(id):
	new = Workout(athlete_id = Athlete.query.get(id).id, date = date.today())
	db.session.add(new)
	db.session.commit()
	flash('Workout added.')
	return redirect(url_for('list_athlete'))


@app.route('/workout/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
	form = WorkoutForm()
	workout = Workout.query.get(id)
	if form.validate_on_submit():
		workout.distance = form.distance.data
		workout.speed = form.speed.data
		workout.date = form.date.data
		workout.note = form.note.data
		db.session.commit()
		flash('Workout updated.')
		return redirect(url_for('view_athlete', id=workout.athlete_id))
	else:
		form.id.data = id
		form.distance.data = workout.distance
		form.speed.data = workout.speed
		form.date.data = workout.date
		form.note.data = workout.note
	return render_template('workout.html', form=form, workout=workout)


@app.route('/workout/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_workout(id):
	delete_workout = Workout.query.get(id)
	db.session.delete(delete_workout)
	db.session.commit()
	flash('Workout deleted.')
	return redirect(url_for('view_athlete', id=delete_workout.athlete_id))


# ##########################
# HELPER
# ##########################
def convert_to_digits(str_of_digits_and_other_chars):
	return ''.join(i for i in str_of_digits_and_other_chars if i.isdigit())

def date_if_older_than_decade(iso_date_str='1900-01-01'):
	current_year = date.today().year
	if iso_date_str.year + 10 < current_year and iso_date_str.year != 1900:
		return iso_date_str
	return None