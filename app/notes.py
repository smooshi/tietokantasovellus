import sqlite3 as sql
from datetime import datetime
import time

def insert_note(user_id, text, isTimed, time, date):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Note (user_id, text, isTimed, time, date) VALUES(?,?,?,?,?)", (user_id, text, isTimed, time, date))
    con.commit()
    con.close()

def select_note_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Note WHERE user_id='%d';" % user_id).fetchall()
    return result

def select_note_by_user_id_and_date(user_id, date):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Note WHERE user_id='%d' AND DATE(date)='%s';" % (user_id, date)).fetchall()
    return result

def select_note_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Note WHERE id='%s';" % id).fetchall()
    return result

def update_note_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Note SET text = '%s' WHERE id='%d';" % (text, id))
        con.commit()

def delete_note(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Note WHERE id='%d';" % (id))
    con.commit()
    con.close()

class Note:
    def __init__(self, user_id, text, isTimed, time, date):
        self.user_id = user_id
        self.text = text
        self.isTimed = isTimed
        self.time = time
        self.date = date

    def __repr__(self):
        return '<Note %r>' % (self.text)