from app import app,lm
from flask import render_template, redirect, request, flash, g, session, url_for
from .forms import LoginForm, UserCreateForm
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta


from models import *
from notes import *

@app.before_request
def before_request():
	g.user = current_user

@app.route('/main')
@login_required
def main():
	user = g.user
	days = set_days(datetime.today().date())
	notes = select_note_by_user_id_and_date(g.user.id, days["today"])
	return render_template('main.html', title='MainPage', user=user, notes=notes, days=days)

@app.route('/timetravel/<date>')
@login_required
def timetravel(date):
	user = g.user

	#emt miksei toimi
	#day = datetime.strptime(str(date),"Y%-%m-%d")
	s = str(date)
	d = datetime.strptime(s, "%Y-%m-%d")
	days = set_days(d.date())

	notes = select_note_by_user_id_and_date(g.user.id, days["today"])

	return render_template('main.html', title='MainPage', user=user, notes=notes, days=days)

def set_days(date):
	t = date+timedelta(days=1)
	y = date+timedelta(days=-1)
	days = {"today":date, "tomorrow": t, "yesterday": y}
	return(days)

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
			update_user_auth(user.id, True)
			#db.session.add(user)
			#db.session.commit()
			#current_user = user
			login_user(user)
			#flash("??? %s %s" %(user.name, user.email))
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
#	return User.query.get(int(id))
#
@app.route('/logout')
def logout():
	user = current_user
	user.authenticated = False
	update_user_auth(user.id, False)
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
		form.flash_errors()
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
			#db.session.add(user)
			#db.session.commit()
			#login_user(user)
		flash("Account succefully created! Try logging in.")
		return redirect(url_for('index'))
	return render_template('create.html', form=form)