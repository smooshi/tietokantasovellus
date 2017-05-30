from flask import render_template, flash, redirect, url_for, g, request, jsonify
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import TodoEditForm, flash_errors
from app.focus import *
from app.todos import *

@app.route('/todo/edit/<id>', methods=['GET', 'POST'])
@login_required
def todo_edit(id):
    user = g.user
    todo = select_todo_by_id(id)
    focus = select_focus_tag_by_todo_id(id)
    if todo == None or todo[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))

    form = TodoEditForm(text=todo[0][2], focus=(focus[0][0] if len(focus)>0 else 0))
    choices = [(0, "Select focus")]
    for row in select_focus_by_user_id(user.id):
        choices.append((row[0], row[2]))
    form.focus.choices = choices
    #form.focus.data = (focus[0][0] if len(focus)>0 else 0)

    if form.validate_on_submit():
        text = form.text.data
        id = todo[0][0]
        update_todo_text(id, text)

        #hmm...
        if form.focus.data != 0:
            if len(focus) > 0:
                delete_focus_tag(id, focus[0][0])
            insert_focus_tag(id, form.focus.data)
        else:
            if len(focus) > 0:
                delete_focus_tag(id, focus[0][0])

        flash("Succefully edited note!")
        flash(form.focus.data)
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/todo/edit.html', todo=todo, user=user, form=form, focus=focus)

@app.route('/todo/add/<date>', methods=['GET', 'POST'])
@login_required
def todo_add(date):
    user = g.user
    form = TodoEditForm()
    choices = [(0, "Select focus")]
    for row in select_focus_by_user_id(user.id):
        choices.append((row[0], row[2]))
    form.focus.choices = choices
    #form.focus.choices = [choices.append((row[0], row[2])) for row in select_focus_by_user_id(user.id)]
    #form.focus.choices= [(row[0], row[2]) for row in select_focus_by_user_id(user.id)]

    s = str(date)
    date = datetime.strptime(s, "%Y-%m-%d")
    if form.validate_on_submit():
        todo_id = insert_todo_return_id(user.id,form.text.data, date)
        if form.focus.data != 0:
            insert_focus_tag(todo_id, form.focus.data)
        flash('Succesfully created todo! ')
        if date.date() == datetime.today().date():
            return redirect(url_for('main'))
        else:
            return redirect(url_for('timetravel', date=date.date()))

    flash_errors(form)
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