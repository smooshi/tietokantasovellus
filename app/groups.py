import sqlite3 as sql
from datetime import datetime

def insert_group(name, description):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Groups (name, description, created_at, edited_at) VALUES(?,?,?,?)", (name, description, datetime.now(), datetime.now()))
    con.commit()
    id = cur.lastrowid
    cur.close()
    con.close()
    return id


def select_all_groups():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Groups;"
        result = cur.execute(com).fetchall()
    return result

def select_group_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM Groups WHERE id=?;"
        result = cur.execute(com, (id,)).fetchall()
    return result

def update_group(name, description, id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "UPDATE Groups SET name = ? AND description = ? AND edited_at = ? WHERE id=?;"
        cur.execute(com, (name, description, datetime.now(), id)).fetchall()
        con.commit()

def insert_user_in_group(user_id, group_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO User_in_Group (user_id, group_id) VALUES(?,?)", (user_id, group_id))
    con.commit()
    con.close()

def insert_user_in_group_admin(user_id, group_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO User_in_Group (user_id, group_id, isAdmin) VALUES(?,?,?)", (user_id, group_id, 1))
    con.commit()
    con.close()

def select_this_users_groups(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM User_in_Group WHERE user_id=?;"
        result = cur.execute(com, (user_id,)).fetchall()
    return result

def select_users_in_group(group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM User_in_Group WHERE group_id=?;"
        result = cur.execute(com, (group_id,)).fetchall()
    return result

def is_user_in_group(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        #com = "SELECT * FROM User_in_Group WHERE group_id=? AND user_id=?;"
        com = "SELECT CASE WHEN EXISTS (SELECT * FROM User_in_Group WHERE group_id=? AND user_id=?) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;"
        result = cur.execute(com, (group_id, user_id)).fetchall()
    return result