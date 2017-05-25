from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from datetime import datetime

def insert_user(name, email, password, authenticated):
    con = sql.connect("database.db")
    cur = con.cursor()
    salt = generate_password_hash(password)
    cur.execute("INSERT INTO User (email, name, salt, authenticated, created_at, edited_at) VALUES(?,?,?,?,?,?)", (email, name, salt, authenticated, datetime.now(), datetime.now()))
    con.commit()
    con.close()

def update_user_auth(id, authenticated):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "UPDATE User SET authenticated =? WHERE id=?;"
    cur.execute(com, (authenticated, id))
    con.commit()
    con.close()

def update_user_no_pw(id, name, email):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "UPDATE User SET name = ?, email= ? WHERE id=?;"
    cur.execute(com, (name, email, id))
    con.commit()
    con.close()

def update_user_pw(id, name, email, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    salt = generate_password_hash(password)
    com = "UPDATE User SET salt='?'' WHERE id=?;"
    cur.execute(com, (salt, id))
    con.commit()
    con.close()

def delete_user(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "DELETE FROM User WHERE id=?;"
    cur.execute(com, (id,))
    con.commit()
    con.close()

def select_by_id_user(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM User WHERE id=?;"
        result = cur.execute(com, (id,)).fetchall()
        if len(result) > 0:
            user = User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
            return user
        else:
            return None

def select_by_name_user(name):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "select * from User where name=?;"
        result = cur.execute(com, (name,)).fetchall()
        if len(result) > 0:
            user = User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
            return user
        else:
            return None

def select_points_from_user(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "select todos, goals, focus from User where id=?;"
        result = cur.execute(com, (id)).fetchall()
        return result

def update_user_todo_points(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "UPDATE User SET todos = todos+1 WHERE id=?;"
    cur.execute(com, (id,)).fetchall()
    con.commit()
    con.close()

def update_user_goal_points(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "UPDATE User SET goals = goals+1 WHERE id=?;"
    cur.execute(com, (id,)).fetchall()
    con.commit()
    con.close()

def update_user_focus_points(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "UPDATE User SET focus = focus+1 WHERE id=?;"
    cur.execute(com, (id,)).fetchall()
    con.commit()
    con.close()

#def select_user_todo_points(id):

class User():

    def __init__(self, id, email, name, salt, authenticated):
        self.id = id
        self.name = name
        self.email = email
        self.salt = salt
        self.authenticated = authenticated;

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