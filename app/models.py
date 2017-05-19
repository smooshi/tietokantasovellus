from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    #password = db.Column(db.String(120))
    salt = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)
        self.authenticated = False

    def set_password(self, password):
        self.salt = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.salt, password)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(160))
    isComplete = db.Column(db.Boolean)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Todo %r>' %(self.text)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(160))
    isTimed = db.Column(db.Boolean)
    time = db.Column(db.DateTime)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Note %r>' %(self.text)