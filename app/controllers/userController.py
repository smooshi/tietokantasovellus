from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required

#models
from app.forms import UserEditForm, flash_errors
from app.models import *
from app.goals import *
from app.discussions import *

#kayttajan profiilisivu
@app.route('/user/<id>')
@login_required
def user(id):
	user = select_by_id_user(id)
	points = select_points_from_user(id)
	goals = select_goals_by_user_id(id)
	if user == None or user.id != g.user.id:
		flash('User not found or allowed.' %(id, g.user.id))
		return redirect(url_for('index'))
	return render_template('/user/profile.html', user=user, points=points, goals=goals)

#kayttajan kommenttiarkisto
@app.route('/user/archive/<id>')
@login_required
def archive(id):
	user = select_by_id_user(id)
	goals = select_goals_by_user_id(id)
	discussions = select_discussions_by_user_id(id)
	if user == None or user.id != g.user.id:
		flash('User not found or allowed.' %(id, g.user.id))
		return redirect(url_for('index'))
	title = "To Do"
	return render_template('/user/archive.html', user=user, goals=goals, discussions=discussions, title=title)

#kayttajan muokkaaminen
@app.route('/user_edit/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
	user = select_by_id_user(id)
	if user == None or user.id != g.user.id:
		flash('User not found.')
		return redirect(url_for('index'))
	form = UserEditForm(username=user.name, email=user.email)
	if form.validate_on_submit():
		update_user_no_pw(user.id, form.username.data, form.email.data)
		flash('Succefully edited user details!')
		return redirect(url_for('user', id=g.user.id))

	#toteuttamatta: salasanan vaihto

	flash_errors(form)
	return render_template('/user/edit.html', user=user, form=form)

#kayttajan poisto
@app.route('/user_delete/<id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
	user = select_by_id_user(id)
	if user == None or user.id != g.user.id:
		flash('Unauthorised enter to user delete.')
		return redirect(url_for('index'))
	flash('Attempted to delete user. (Not implemented)')
	return redirect(url_for('index'))