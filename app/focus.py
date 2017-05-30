import sqlite3 as sql
from datetime import datetime

def insert_focus(user_id, text):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Focus (user_id, text, created_at) VALUES(?,?,?)", (user_id, text, datetime.now()))
    con.commit()
    con.close()

def select_focus_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Focus WHERE user_id=?;"
        result = cur.execute("SELECT * FROM Focus WHERE user_id=?;", (user_id,)).fetchall()
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
        cur.execute("UPDATE Focus SET text = ? WHERE id=?;", (text, id))
        con.commit()

def delete_focus(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Focus WHERE id=?;", (id,))
    con.commit()
    con.close()

def update_focus_points(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Focus SET points = points+1 WHERE id=?;", (id,))
        con.commit()

def insert_focus_tag(todo_id, focus_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Focus_Tag (todo_id, focus_id) VALUES(?,?)", (todo_id, focus_id))
    con.commit()
    con.close()

def select_focus_tag_by_todo_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        #com = "SELECT u.* FROM User u INNER JOIN User_in_Group ug ON u.id=ug.user_id WHERE ug.group_id=?;"
        com = "SELECT f.* FROM Focus f INNER JOIN Focus_Tag ft ON f.id=ft.focus_id WHERE ft.todo_id=?;"
        result = cur.execute(com, (id,)).fetchall()
    return result

def select_focus_tag_by_focus_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Focus_Tag WHERE focus_id=?;"
        result = cur.execute(com, (id,)).fetchall()
    return result

def delete_focus_tag(todo_id, focus_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Focus_Tag WHERE todo_id=? AND focus_id=?;", (todo_id,focus_id))
    con.commit()
    con.close()
