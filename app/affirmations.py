import sqlite3 as sql
from datetime import datetime

#Affirmatioiden modeli eli tietokantakutsut

def insert_affirmation(user_id, text, date):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Affirmation (user_id, text, date) VALUES(?,?,?)", (user_id, text, date))
    con.commit()
    con.close()

def select_affirmation_by_user_id(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Affirmation WHERE user_id=?;", (user_id,)).fetchall()
    return result

def select_affirmation_by_user_id_and_date(user_id, date):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Affirmation WHERE user_id=? AND DATE(date)=?;", (user_id, date)).fetchall()
    return result

def select_affirmation_by_id(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Affirmation WHERE id=?;", (id,)).fetchall()
    return result

def update_affirmation_text(id, text):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE Affirmation SET text = ? WHERE id=?;", (text, id))
        con.commit()

def delete_affirmation(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Affirmation WHERE id=?;", (id,))
    con.commit()
    con.close()