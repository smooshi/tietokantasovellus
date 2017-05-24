from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required

#models
from app.forms import UserEditForm, FlashErrors
from app.models import *
from app.goals import *

@app.route('/user/<id>')
@login_required
def user(id):
	user = select_by_id_user(id)
	points = select_points_from_user(id)
	goals = select_goals_by_user_id(id)
	if user == None or user.id != g.user.id:
		flash('User not found or allowed.' %(id, g.user.id))
		return redirect(url_for('index'))
	FlashErrors.flash_errors(form)
	return render_template('profile.html', user=user, points=points, goals=goals)

@app.route('/user_edit/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
	user = select_by_id_user(id)
	if user == None or user.id != g.user.id:
		flash('User not found.')
		return redirect(url_for('index'))
	form = UserEditForm(username=user.name, email=user.email)
	if form.validate_on_submit():
#		if user.check_password(form.confirm.data):
#			if form.password.data is not None or form.password.data != "":
#				flash('User with pw --->  %s.' % (form.password.data))
#				#update_user_with_pw(user.id, form.username.data, form.email.data, form.password.data )
#			else:
#				flash('User wo pw')
		update_user_no_pw(user.id, form.username.data, form.email.data)
		flash('Succefully edited user details!')
		return redirect(url_for('user', id=g.user.id))


	FlashErrors.flash_errors(form)
	return render_template('/user/edit.html', user=user, form=form)

@app.route('/user_delete/<id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
	user = select_by_id_user(id)
	if user == None or user.id != g.user.id:
		flash('Unauthorised enter to user delete.')
		return redirect(url_for('index'))
	flash('Attempted to delete user')
	return redirect(url_for('index'))