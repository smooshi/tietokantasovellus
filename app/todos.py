import sqlite3 as sql
from datetime import datetime
import time

def insert_todo(user_id, text, isComplete, date):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Todo (user_id, text, isComplete, date) VALUES(?,?,?,?)", (user_id, text, isComplete, date))
    con.commit()
    con.close()

def select_todo_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Todo WHERE user_id='%d';" % user_id).fetchall()
    return result

def select_todo_by_user_id_and_date(user_id, date):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Todo WHERE user_id='%d' AND DATE(date)='%s';" % (user_id, date)).fetchall()
    return result

def select_todo_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Todo WHERE id='%s';" % id).fetchall()
    return result

def update_todo_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Todo SET text = '%s' WHERE id='%d';" % (text, id))
        con.commit()

def update_todo_complete(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Todo SET isComplete = 1 WHERE id='%d';" % (id))
        con.commit()

def update_todo_uncomplete(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Todo SET isComplete = 0 WHERE id='%d';" % (id))
        con.commit()

def delete_todo(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Todo WHERE id='%d';" % (id))
    con.commit()
    con.close()