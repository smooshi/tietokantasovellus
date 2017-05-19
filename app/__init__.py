from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from flask.ext.login import LoginManager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = "Please login to view main page."

#last
from app import views, models