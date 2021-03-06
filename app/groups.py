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

def select_group_by_name(name):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT Groups.name FROM Groups WHERE name=?;"
        result = cur.execute(com, (name,)).fetchall()
        if len(result) > 0:
            return result
        else:
            return None

def update_group(name, description, id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "UPDATE Groups SET name = ?, description = ?, edited_at = ? WHERE id=?;"
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

def is_user_in_group(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT CASE WHEN EXISTS (SELECT * FROM User_in_Group WHERE group_id=? AND user_id=?) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;"
        result = cur.execute(com, (group_id, user_id)).fetchall()
    return result

def is_user_group_admin(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT CASE WHEN EXISTS (SELECT * FROM User_in_Group WHERE group_id=? AND user_id=? AND isAdmin=1) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;"
        result = cur.execute(com, (group_id, user_id)).fetchall()
    return result

def update_group_user_to_admin(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "UPDATE User_in_Group SET isAdmin=1 WHERE user_id=? AND group_id=?;"
        cur.execute(com, (user_id, group_id)).fetchall()
        con.commit()

def update_group_user_to_not_admin(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "UPDATE User_in_Group SET isAdmin=0 WHERE user_id=? AND group_id=?;"
        cur.execute(com, (user_id, group_id)).fetchall()
        con.commit()

def select_groups_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        #com = "SELECT * FROM Groups INNER JOIN User_in_Group ON Groups.id = User_in_Group.group_id WHERE User_in_Group.user_id = ?;"
        com = "SELECT g.* FROM Groups g INNER JOIN User_in_Group ug ON g.id=ug.group_id WHERE ug.user_id=?;"
        result = cur.execute(com, (user_id,)).fetchall()
    return result

def select_group_admins(group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT User_in_Group.user_id FROM User_in_Group WHERE group_id=? AND isAdmin=1;"
        result = cur.execute(com, (group_id,)).fetchall()
    return result

def select_users_by_group_id(group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        #com = "SELECT * FROM User INNER JOIN User_in_Group ON User.id = User_in_Group.user_id WHERE User_in_Group.group_id = ?;"
        com = "SELECT u.* FROM User u INNER JOIN User_in_Group ug ON u.id=ug.user_id WHERE ug.group_id=?;"
        result = cur.execute(com, (group_id,)).fetchall()
    return result

def delete_user_in_group(user_id, group_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "DELETE FROM User_in_Group WHERE group_id=? AND user_id=?;"
    cur.execute(com, (group_id,user_id))
    con.commit()
    con.close()

def delete_group(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    com = "DELETE FROM Groups WHERE id=?;"
    cur.execute(com, (id,))
    con.commit()
    con.close()