from app import app,lm
from flask import render_template, redirect, request, flash, g, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from operator import itemgetter

from app.forms import LoginForm, UserCreateForm, flash_errors
from app.models import *
from app.notes import *
from app.todos import *
from app.goals import *
from app.focus import *
from app.groups import *
from app.discussions import *

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
	todot = select_todo_by_user_id_and_date(g.user.id, days["today"])
	todos = sorted(todot, key=itemgetter(3))
	goals = select_current_goal_by_user_id(g.user.id)
	focus = select_focus_by_user_id(g.user.id)
	groups = select_groups_by_user_id(g.user.id)
	latest = get_latest_discussions(groups)
	todo_focus = get_todo_focus(todot)

	#on taysin mahdollista etta taman voi tehda paremmin
	if request.method == 'POST':
		# todo completion:
		rq = request.form.getlist('check')
		if (len(rq)>0):
			update_todo_complete(int(rq[0]))
			update_user_todo_points(g.user.id)

			#update focus that todo is linked with if todo is linked with focus
			f = select_focus_tag_by_todo_id(int(rq[0]))
			if len(f) > 0:
				update_focus_points(f[0][0])
				update_user_focus_points(g.user.id)
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

	return render_template('main.html', title='MainPage', user=user, tnotes= timed, notes=notTimed, days=days, todos=todos, goals=goals, focus=focus, groups=groups, latest=latest, todo_focus=todo_focus)

#talle tarvitaan parempi ratkaisu, tama on kontrolleri joka nayttaa "eri paivia", mutta kayttaa kuitenkin main.html sivua
@app.route('/timetravel/<date>', methods=['GET', 'POST'])
@login_required
def timetravel(date):
	user = g.user
	#emt miksei toimi
	#day = datetime.strptime(str(date),"Y%-%m-%d")
	s = str(date)
	d = datetime.strptime(s, "%Y-%m-%d")
	days = set_days(d.date())

	#Return to main if date is "today"
	if d.date() == datetime.now().date():
		return redirect(url_for('main'))

	notes = select_note_by_user_id_and_date(g.user.id, days["today"])
	timed, notTimed = sort_notes(notes)
	todos = select_todo_by_user_id_and_date(g.user.id, days["today"])
	goals = select_current_goal_by_user_id(g.user.id)
	focus = select_focus_by_user_id(g.user.id)
	groups = select_groups_by_user_id(g.user.id)
	latest = get_latest_discussions(groups)

	if request.method == 'POST':
		#Todo complete estetty
		flash("That's currently disabled.")

	return render_template('main.html', title='MainPage', user=user, tnotes= timed, notes=notTimed, days=days, todos=todos, goals=goals, groups=groups, focus=focus, latest=latest)

#Set yesterday,today, tomorrow into dictionary
def set_days(date):
	t = date+timedelta(days=1)
	y = date+timedelta(days=-1)
	days = {"today":date, "tomorrow": t, "yesterday": y}
	return(days)

#Sort notes into right order and two different arrays for display on page
def sort_notes(notes):
	timed = list()
	notTimed = list()
	for i in range (0, len(notes)):
		arr = list(notes[i])
		if arr[3] == 1:
			s = arr[4]
			d = datetime.strptime(str(s), "%Y-%m-%d %H:%M:%S")
			arr[4]=d.time()
			timed.append(arr)
		else:
			notTimed.append(arr)

	timed = sorted(timed, key=itemgetter(4))
	return timed, notTimed

#set the latest post in group to dict where key is group id
def get_latest_discussions(groups):
	latest = {}
	for i in range(0, len(groups)):
		latest[groups[i][0]] = latest_discussion_in_group(groups[i][0])
	return latest

#set todo tags into dict where key is todo id
def get_todo_focus(todos):
	todo_focus = {}
	for i in range(0, len(todos)):
		focus =  select_focus_tag_by_todo_id(todos[i][0])
		if (focus != None and len(focus) != 0):
			todo_focus[todos[i][0]] = focus[0][2]
		else:
			todo_focus[todos[i][0]] = " "
	return todo_focus

@app.route('/')
@app.route('/index')
def index():
	if g.user is not None and g.user.is_authenticated:
 		return redirect(url_for('main'))
 	return render_template('index.html', title='index')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('main'))
	form = LoginForm()
	if form.validate_on_submit():
		#session['remember_me'] = form.remember_me.data
		return try_login(form.username.data, form.password.data)
	flash_errors(form)
	return render_template('login.html', form=form)

#Login logiikka
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

#Required for login manager
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