from flask import render_template
from flask import flash
from flask import redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='index')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login name="%s",remember_me=%s' % (form.uname.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html', form=form)