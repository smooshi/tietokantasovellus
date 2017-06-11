import sqlite3 as sql
from datetime import datetime

def insert_discussion(user_id, group_id, title, text):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO GroupDiscussion (user_id, group_id, title, text, created_at, edited_at) VALUES(?,?,?,?,?,?)", (user_id, group_id, title, text, datetime.now(), datetime.now()))
    con.commit()
    con.close()

def select_discussion_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM GroupDiscussion WHERE id=?;", (id,)).fetchall()
    return result

def update_discussion_text(id, title, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE GroupDiscussion SET text = ?, title=?, edited_at=? WHERE id=?;", (text, title, datetime.now(), id))
        con.commit()

def delete_discussion(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM GroupDiscussion WHERE id=?;", (id,))
    con.commit()
    con.close()

def select_discussions_from_user_in_group(user_id, group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM GroupDicussion WHERE user_id=? AND group_id=?;"
        result = cur.execute(com, (user_id,group_id)).fetchall()
    return result

def select_discussions_from_user(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM GroupDicussion WHERE user_id=?;"
        result = cur.execute(com, (user_id,)).fetchall()
    return result

def select_discussion_by_group_id(group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT gd.*, u.name FROM GroupDiscussion gd JOIN User u ON u.id=gd.user_id WHERE gd.group_id=?;"
        result = cur.execute(com, (group_id,)).fetchall()
    return result

def latest_discussion_in_group(group_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        #com = "SELECT * FROM GroupDiscussion WHERE  id = (SELECT MAX(id) FROM GroupDiscussion WHERE group_id=?);"
        com = "SELECT gd.*, u.name FROM GroupDiscussion gd JOIN User u ON u.id=gd.user_id WHERE gd.id = (SELECT MAX(gd.id) FROM  GroupDiscussion gd WHERE group_id=?);"
        result = cur.execute(com, (group_id,)).fetchall()
    return result

def latest_discussion_by_user(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        com = "SELECT * FROM GroupDiscussion WHERE  id = (SELECT MAX(id) FROM GroupDiscussion WHERE user_id=?)"
        result = cur.execute(com, (user_id,)).fetchall()
    return result

def select_discussions_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT gd.*, g.name FROM GroupDiscussion gd JOIN Groups g ON gd.group_id=g.id WHERE user_id=?;", (user_id,)).fetchall()
    return result