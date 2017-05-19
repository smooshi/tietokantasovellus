from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from .forms import LoginForm, CreateForm
from flask_login import login_user, logout_user, current_user, login_required

#models
from .models import User



@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	return render_template('index.html', title='index', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return try_login(form.username.data, form.password.data)
	return render_template('login.html', form=form)

def try_login(username, password):
	if username is None or username =="":
		flash('Invalid username. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter(User.name==username).first()
	if user is None:
		flash('User does not exist. Please try again.')
		return redirect(url_for('login'))
	else:
		if (user.check_password(password)):
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)
				login_user(user, remember = remember_me)
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash('Password is wrong. Please try again.')
			return redirect(url_for('login'))
	#return render_template('login.html', form=form)

@app.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = CreateForm()
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

		user = User(name=username, email=email, password=password)
		if (user.check_password(password)):
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('index'))
	return render_template('create.html', form=form)