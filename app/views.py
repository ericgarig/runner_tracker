from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_user, logout_user, login_required
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
			return redirect(url_for('index'))
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
@app.route('/athlete/list')
@login_required
def index():
	athletes = Athlete.query.get(1)
	return render_template('index.html', athletes=athletes)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def create_athlete():
	form = EditForm()
	if form.validate_on_submit():
		new = Athlete(name_first=form.name_first.data,
						name_last=form.name_last.data,
						phone_number =convert_to_digits(form.phone_number.data),
						email=form.email.data,
						date_birth=form.date_birth.data,
						disability=form.disability.data,
						pace=form.pace.data,
						address_street=form.address_street.data,
						address_city=form.address_city.data,
						address_state=form.address_state.data,
						address_zip=form.address_zip.data,
						ice_name=form.ice_name.data,
						ice_phone=convert_to_digits(form.ice_phone.data),
						note=form.note.data
						)
		db.session.add(new)
		db.session.commit()
		flash('New athlete created.')
		return redirect(url_for('index'))
	else:
		form.id.data = 0
		form.name_first.data = ''
		form.name_last.data = ''
		form.phone_number.data = ''
		form.ice_phone.data = ''
		form.ice_name.data = ''
	return render_template('athlete_create.html', form=form)


@app.route('/athlete/<int:id>/view')
@login_required
def view_athlete(id):
	athlete = Athlete.query.get(id)
	return render_template('athlete_view.html', athlete=athlete)


@app.route('/athlete/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_athlete(id):
	form = EditForm()
	athlete = Athlete.query.get(id)
	if form.validate_on_submit():
		athlete.name_first = form.name_first.data
		athlete.name_last = form.name_last.data
		athlete.phone_number = convert_to_digits(form.phone_number.data)
		athlete.ice_phone = convert_to_digits(form.ice_phone.data)
		athlete.ice_name = form.ice_name.data
		db.session.commit()
		flash('Athlete info updated.')
		return redirect(url_for('view_athlete', id=athlete.id))
	else:
		form.id.data = id
		form.name_first.data = athlete.name_first
		form.name_last.data = athlete.name_last
		form.phone_number.data = athlete.phone_number
		form.ice_phone.data = athlete.ice_phone
		form.ice_name.data = athlete.ice_name
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
			return redirect(url_for('index'))
		else:
			form.id.data = id
			flash('Please type in the first and last name to confirm delering of %s.' % (athlete.name_fl()))
	return render_template('athlete_delete.html', form=form, athlete=athlete)


# ##########################
# WORKOUT
# ##########################
@app.route('/workout/create_for/<int:id>', methods=['GET', 'POST'])
@login_required
def new_workout(id):
	new = Workout(athlete_id = Athlete.query.get(id).id, date = date.today())
	db.session.add(new)
	db.session.commit()
	flash('Workout added.')
	return redirect(url_for('index'))


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

