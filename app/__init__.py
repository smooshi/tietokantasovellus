from flask import Flask
import sys
import logging
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()


#Errors for Heroku
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

#Login handling
from flask.ext.login import LoginManager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = "Please login first."

#last
from app import views, models
from app.controllers import *