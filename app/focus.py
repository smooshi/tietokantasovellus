import sqlite3 as sql
from datetime import datetime

def insert_focus(user_id, text, end_date):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Focus (user_id, text, created_at, edited_at, end_date) VALUES(?,?,?,?,?)", (user_id, text, datetime.now(), datetime.now(), end_date))
    con.commit()
    con.close()

def select_focus_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Focus WHERE user_id=?;"
        result = cur.execute("SELECT * FROM Focus WHERE user_id=?;", (user_id,)).fetchall()
    return result

def select_current_focus_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Focus WHERE user_id=? AND isActive;", (user_id,)).fetchall()
    return result

def select_focus_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Focus WHERE id=?;"
        result = cur.execute(com, (id,)).fetchall()
    return result

def update_focus_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Focus SET text = ? , edited_at=? WHERE id=?;", (text, datetime.now(), id))
        con.commit()

def delete_focus(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Focus WHERE id=?;", (id,))
    con.commit()
    con.close()

def update_focus_active(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Focus SET isActive = 1 WHERE id=?;", (id,))
        con.commit()

def update_focus_deactivate(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Focus SET isActive = 0 WHERE id=?;", (id,))
        con.commit()

def update_focus_points(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Focus SET points = points+1 WHERE id=?;", (id,))
        con.commit()