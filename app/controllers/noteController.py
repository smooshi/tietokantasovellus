from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required

#models
from app.forms import NoteEditForm, FlashErrors
from app.notes import *

@app.route('/note/edit/<id>', methods=['GET', 'POST'])
@login_required
def note_edit(id):
    user = g.user
    note = select_note_by_id(id)
    if note == None or note[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))
    form = NoteEditForm(text=note[0][2])
    if form.validate_on_submit():
        text = form.text.data
        id = note[0][0]
        update_note_text(id, text)
        flash("Succefully edited note!")
        return redirect(url_for('main'))
    FlashErrors.flash_errors(form)
    return render_template('/note/edit.html', note=note, user=user, form=form)

@app.route('/note/add/<date>', methods=['GET', 'POST'])
@login_required
def note_add(date):
    user = g.user
    form = NoteEditForm()
    s = str(date)
    date = datetime.strptime(s, "%Y-%m-%d")
    if form.validate_on_submit():
        #time:
        if (form.isTimed.data):
            if (form.time.data is not None):
                time = form.time.data
                time = datetime.combine(date, time)
                insert_note(user.id,form.text.data,form.isTimed.data, time,date)
            else:
                flash('Add time if note is timed.')
                return render_template('/note/add.html', user=user, form=form)
        else:
            insert_note(user.id, form.text.data, form.isTimed.data, None, date)

        flash('Succesfully created note!')
        if date.date() == datetime.today().date():
            return redirect(url_for('main'))
        else:
            return redirect(url_for('timetravel', date=date.date()))

    FlashErrors.flash_errors(form)
    return render_template('/note/add.html', user=user, form=form)

@app.route('/note/delete/<id>', methods=['GET', 'POST'])
@login_required
def note_delete(id):
    note = select_note_by_id(id)
    if note == None or note[0][1] != g.user.id:
        flash('Unauthorised enter to user delete.')
        return redirect(url_for('index'))
    delete_note(note[0][0])
    flash("Succesfully deleted note.")

    s = str(note[0][5])
    date = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

    if date.date() == datetime.today().date():
        return redirect(url_for('main'))
    else:
        return redirect(url_for('timetravel', date=date.date()))
    #return redirect(url_for('main'))