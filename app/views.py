from flask import render_template, flash, redirect, session, url_for, request
from datetime import date
from app import app, db
from .forms import EditForm, DeleteForm, WorkoutForm
from .models import Athlete, Workout


@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
	athletes = Athlete.query.get(1)
	return render_template('index.html', athletes=athletes)


@app.route('/new', methods=['GET', 'POST'])
def create_athlete():
	form = EditForm()
	if form.validate_on_submit():
		new = Athlete(name_first=form.name_first.data,
						name_last=form.name_last.data,
						phone_number =form.phone_number.data,
						ice_phone=form.ice_phone.data,
						ice_name=form.ice_name.data)
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


@app.route('/view/<int:id>')
def view_athlete(id):
	athlete = Athlete.query.get(id)
	return render_template('athlete_view.html', athlete=athlete)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_athlete(id):
	form = EditForm()
	athlete = Athlete.query.get(id)
	if form.validate_on_submit():
		athlete.name_first = form.name_first.data
		athlete.name_last = form.name_last.data
		athlete.phone_number = form.phone_number.data
		athlete.ice_phone = form.ice_phone.data
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


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
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


@app.route('/workout/<int:id>', methods=['GET', 'POST'])
def new_workout(id):
	new = Workout(athlete_id = Athlete.query.get(id).id, date = date.today())
	db.session.add(new)
	db.session.commit()
	flash('Workout added.')
	return redirect(url_for('index'))


@app.route('/edit_workout/<int:id>', methods=['GET', 'POST'])
def edit_workout(id):
	form = WorkoutForm()
	workout = Workout.query.get(id)
	if form.validate_on_submit():
		workout.distance = form.distance.data
		workout.speed = form.speed.data
		workout.date = form.date.data
		db.session.commit()
		flash('Workout updated.')
		return redirect(url_for('view_athlete', id=workout.athlete_id))
	else:
		form.id.data = id
		form.distance.data = workout.distance
		form.speed.data = workout.speed
		form.date.data = workout.date
	return render_template('workout.html', form=form, workout=workout)


@app.route('/delete_workout/<int:id>', methods=['GET', 'POST'])
def delete_workout(id):
	delete_workout = Workout.query.get(id)
	db.session.delete(delete_workout)
	db.session.commit()
	flash('Workout deleted.')
	return redirect(url_for('view_athlete', id=delete_workout.athlete_id))
