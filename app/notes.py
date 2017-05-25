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
        result = cur.execute("SELECT * FROM Note WHERE user_id=?;", (user_id,)).fetchall()
    return result

def select_note_by_user_id_and_date(user_id, date):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Note WHERE user_id=? AND DATE(date)=?;", (user_id, date)).fetchall()
    return result

def select_note_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Note WHERE id=?;", (id,)).fetchall()
    return result

def update_note_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Note SET text = ? WHERE id=?;", (text, id))
        con.commit()

def update_note_text_time(id, text, isTimed, time):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Note SET text = ?, isTimed = ?, DATETIME(time)=? WHERE id=?;", (text, isTimed, time, id))
        con.commit()

def delete_note(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Note WHERE id=?;", (id,))
    con.commit()
    con.close()