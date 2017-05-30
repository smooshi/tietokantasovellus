from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import FocusAddForm, FocusEditForm, flash_errors
from app.focus import *

@app.route('/focus_edit/<id>', methods=['GET', 'POST'])
@login_required
def focus_edit(id):
    user = g.user
    focus = select_focus_by_id(id)
    if focus == None or focus[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))
    form = FocusEditForm(text=focus[0][2])
    if form.validate_on_submit():
        if (form.isActive.data == focus[0][4]):
            update_focus_text(focus[0][0], form.text.data)
            flash('Updated focus!')
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/focus/edit.html', user=user, focus=focus, form=form)

@app.route('/focus_add/', methods=['GET', 'POST'])
@login_required
def focus_add():
    user = g.user
    form = FocusAddForm()
    if form.validate_on_submit():
        insert_focus(g.user.id, form.text.data)
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/focus/add.html', user=user, form=form)

@app.route('/focus/delete/<id>', methods=['GET', 'POST'])
@login_required
def focus_delete(id):
    focus = select_focus_by_id(id)
    if focus == None or focus[0][1] != g.user.id:
        flash('Unauthorised enter to user delete.')
        return redirect(url_for('index'))
    delete_focus(focus[0][0])
    flash("Succesfully deleted focus.")
    return redirect(url_for('main'))