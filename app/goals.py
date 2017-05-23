import sqlite3 as sql
from datetime import datetime

def insert_goal(user_id, text, end_date):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Goal (user_id, text, created_at, edited_at, end_date) VALUES(?,?,?,?,?)", (user_id, text, datetime.now(), datetime.now(), end_date))
    con.commit()
    con.close()

def select_goals_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Goal WHERE user_id=?;"
        result = cur.execute("SELECT * FROM Goal WHERE user_id=?;", (user_id,)).fetchall()
    return result

def select_current_goal_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Goal WHERE user_id=? AND isActive;", (user_id,)).fetchall()
    return result

def select_goal_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Goal WHERE id=?;"
        result = cur.execute(com, (id,)).fetchall()
    return result

def update_goal_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Goal SET text = ? , edited_at=? WHERE id=?;", (text, datetime.now(), id))
        con.commit()

def delete_goal(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Goal WHERE id=?;", (id))
    con.commit()
    con.close()

def update_goal_active(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Goal SET isActive = 1 WHERE id=?;", (id,))
        con.commit()

def update_goal_deactivate(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Goal SET isActive = 0 WHERE id=?;", (id))
        con.commit()