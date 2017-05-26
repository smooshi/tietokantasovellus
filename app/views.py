from app import app,lm
from flask import render_template, redirect, request, flash, g, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from operator import itemgetter

from .forms import LoginForm, UserCreateForm, flash_errors
from models import *
from notes import *
from todos import *
from goals import *
from focus import *
from groups import *

@app.before_request
def before_request():
	g.user = current_user

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
	user = g.user
	days = set_days(datetime.today().date())
	notes = select_note_by_user_id_and_date(g.user.id, days["today"])
	timed, notTimed = sort_notes(notes)
	todos = select_todo_by_user_id_and_date(g.user.id, days["today"])
	todos = sorted(todos, key=itemgetter(3))
	goals = select_current_goal_by_user_id(g.user.id)
	focus = select_current_focus_by_user_id(g.user.id)
	groups = select_groups_by_user_id(g.user.id)

	#on taysin mahdollista etta taman voi tehda paremmin
	if request.method == 'POST':
		# todo completion:
		rq = request.form.getlist('check')
		if (len(rq)>0):
			update_todo_complete(int(rq[0]))
			update_user_todo_points(g.user.id)
			return redirect(url_for('main'))

		# goal points
		gl = request.form.getlist('goal')
		if (len(gl)>0):
			#flash(gl[0])
			update_goal_points(gl[0])
			update_user_goal_points(g.user.id)
			return redirect(url_for('main'))

		#focus points
		fp = request.form.getlist('focus')
		if (len(fp) >0):
			update_focus_points(fp[0])
			update_user_focus_points(g.user.id)
			return redirect(url_for('main'))

	return render_template('main.html', title='MainPage', user=user, tnotes= timed, notes=notTimed, days=days, todos=todos, goals=goals, focus=focus, groups=groups)

#talle tarvitaan parempi ratkaisu
@app.route('/timetravel/<date>', methods=['GET', 'POST'])
@login_required
def timetravel(date):
	user = g.user
	#emt miksei toimi
	#day = datetime.strptime(str(date),"Y%-%m-%d")
	s = str(date)
	d = datetime.strptime(s, "%Y-%m-%d")
	days = set_days(d.date())

	if (days["today"] == datetime.now().date):
		return redirect(url_for('main'))

	notes = select_note_by_user_id_and_date(g.user.id, days["today"])
	timed, notTimed = sort_notes(notes)
	todos = select_todo_by_user_id_and_date(g.user.id, days["today"])
	goals = select_current_goal_by_user_id(g.user.id)
	focus = select_current_focus_by_user_id(g.user.id)
	groups = select_groups_by_user_id(g.user.id)

	if request.method == 'POST':
		#Todo complete estetty
		flash("That's currently disabled.")

	return render_template('main.html', title='MainPage', user=user, tnotes= timed, notes=notTimed, days=days, todos=todos, goals=goals, groups=groups, focus=focus)

def set_days(date):
	t = date+timedelta(days=1)
	y = date+timedelta(days=-1)
	days = {"today":date, "tomorrow": t, "yesterday": y}
	return(days)

def sort_notes(notes):
	timed = list()
	notTimed = list()
	for i in range (0, len(notes)):
		arr = list(notes[i])
		if arr[3] == 1:
			s = arr[4]
			d = datetime.strptime(str(s), "%Y-%m-%d %H:%M:%S")
			t = d.time()
			arr[4]=t
			timed.append(arr)
		else:
			notTimed.append(arr)

	timed = sorted(timed, key=itemgetter(4))
	return timed, notTimed

@app.route('/')
@app.route('/index')
def index():
 	#if current_user.is_authenticated and current_user is not None:
 	#	return redirect(url_for('main'))
	if g.user is not None and g.user.is_authenticated:
 		return redirect(url_for('main'))
 	return render_template('index.html', title='index')

@app.route('/login', methods=['GET', 'POST'])
def login():
	#if current_user.is_authenticated and current_user is not None:
	#	return redirect(url_for('main'))
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('main'))
	form = LoginForm()
	if form.validate_on_submit():
		#session['remember_me'] = form.remember_me.data
		return try_login(form.username.data, form.password.data)
	flash_errors(form)
	return render_template('login.html', form=form)

def try_login(username, password):
	if username is None or username =="":
		flash('Invalid username. Please try again.')
		return redirect(url_for('login'))
	user = select_by_name_user(username)
	if user is None:
		flash('User does not exist. Please try again.')
		return redirect(url_for('login'))
	else:
		if (user.check_password(password)):
			#if 'remember_me' in session:
			#	remember_me = session['remember_me']
			#	session.pop('remember_me', None)
			user.authenticated = True
			update_user_auth(user.id, 1)
			login_user(user)
			return redirect(request.args.get('next') or url_for('main'))
		else:
			flash('Password is wrong. Please try again.')
			return redirect(url_for('login'))
#
@lm.user_loader
def load_user(id):
	user = select_by_id_user(id)
	if user != None:
		return (user)
	else:
		return (None)

@app.route('/logout')
def logout():
	user = current_user
	user.authenticated = False
	update_user_auth(user.id, 0)
	logout_user()
	return redirect(url_for('index'))
#
@app.route('/create', methods=['GET', 'POST'])
def create():
	#if current_user.is_authenticated:
	#	return redirect(url_for('main'))
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('main'))
	form = UserCreateForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		email = form.email.data
		if username is None or username == "":
			flash('Invalid username. Please try again.')
			return redirect(url_for('create'))
		if password is None or password == "":
			flash('Invalid password. Please try again.')
			return redirect(url_for('create'))
		if email is None or email == "":
			flash('Invalid email. Please try again.')
			return redirect(url_for('create'))

		insert_user(username, email, password, True)
		#login_user(user)
		flash("Account succefully created! Try logging in.")
		return redirect(url_for('index'))
	flash_errors(form)
	return render_template('create.html', form=form)