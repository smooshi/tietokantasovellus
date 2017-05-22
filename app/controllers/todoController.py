from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import TodoEditForm
from app.models import *
from app.todos import *

@app.route('/todo/edit/<id>', methods=['GET', 'POST'])
@login_required
def todo_edit(id):
    user = g.user
    todo = select_todo_by_id(id)
    if todo == None or todo[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))
    form = TodoEditForm(text=todo[0][2])
    if form.validate_on_submit():
        text = form.text.data
        id = todo[0][0]
        update_todo_text(id, text)
        flash("Succefully edited note!")
        return redirect(url_for('main'))
    return render_template('/todo/edit.html', todo=todo, user=user, form=form)

@app.route('/todo/add/<date>', methods=['GET', 'POST'])
@login_required
def todo_add(date):
    user = g.user
    form = TodoEditForm()
    s = str(date)
    date = datetime.strptime(s, "%Y-%m-%d")
    if form.validate_on_submit():
        insert_todo(user.id,form.text.data, False, date)

        flash('Succesfully created note!')
        if date.date() == datetime.today().date():
            return redirect(url_for('main'))
        else:
            return redirect(url_for('timetravel', date=date.date()))

    return render_template('/todo/add.html', user=user, form=form)

@app.route('/todo/delete/<id>', methods=['GET', 'POST'])
@login_required
def todo_delete(id):
    todo = select_todo_by_id(id)
    if todo == None or todo[0][1] != g.user.id:
        flash('Unauthorised enter to user delete.')
        return redirect(url_for('index'))
    delete_todo(todo[0][0])
    flash("Succesfully deleted note.")

    s = str(todo[0][4])
    date = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

    if date.date() == datetime.today().date():
        return redirect(url_for('main'))
    else:
        return redirect(url_for('timetravel', date=date.date()))
    #return redirect(url_for('main'))