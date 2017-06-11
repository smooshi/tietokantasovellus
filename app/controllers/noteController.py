from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import NoteEditForm, flash_errors
from app.notes import *

#notejen muokkaus
@app.route('/note/edit/<id>', methods=['GET', 'POST'])
@login_required
def note_edit(id):
    user = g.user
    note = select_note_by_id(id)
    if note == None or note[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))

    #aikojen muokkaus, yritetään myös ylläpitää päivää.
    if note[0][3] == 1:
        d = datetime.strptime(str(note[0][4]), "%Y-%m-%d %H:%M:%S")
        time = d.time()
    else:
        #korjattava: jos aikaa ei ole määritelty aiemmin mutta muokataan todoa x päivässä, aikaa ei saa oikein sille paivalle vaan asetetaan nyt aika.
        #se pitaa tuoda jostain muualta
        d = datetime.now()
        time = datetime(2017, 01, 01, 00, 00, 00)
        time = time.time()

    form = NoteEditForm(text=note[0][2], isTimed=note[0][3], time=time)
    if form.validate_on_submit():
        id = note[0][0]
        if form.isTimed.data != note[0][3] or form.time.data != time:
            time = datetime.combine(d, form.time.data)
            update_note_text_time(id, form.text.data, form.isTimed.data, time)
        else:
            update_note_text(id, form.text.data)
        flash("Succefully edited note!")
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/note/edit.html', note=note, user=user, form=form)

#notejen lisays
@app.route('/note/add/<date>', methods=['GET', 'POST'])
@login_required
def note_add(date):
    user = g.user
    time = datetime(2017,01,01,00,00,00)
    form = NoteEditForm(time=time.time())
    s = str(date)
    date = datetime.strptime(s, "%Y-%m-%d")
    if form.validate_on_submit():
        #time:
        if (form.isTimed.data):
            if (form.time.data is not None):
                time = form.time.data
                time = datetime.combine(date, time)
                insert_note(user.id,form.text.data,form.isTimed.data, time, date)
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

    flash_errors(form)
    return render_template('/note/add.html', user=user, form=form)

#notejen poisto
@app.route('/note/delete/<id>', methods=['GET', 'POST'])
@login_required
def note_delete(id):
    note = select_note_by_id(id)
    if note == None or note[0][1] != g.user.id:
        flash('Unauthorised enter to note delete.')
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