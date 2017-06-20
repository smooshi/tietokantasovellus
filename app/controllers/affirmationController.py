from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import AffirmationEditForm, flash_errors
from app.affirmations import *

#Affirmation kontrolleri:
#affirmaatioiden lisays ja deletointi tehdaan taalla, mutta kokeilusyista lisays tehdaan views.py:ssa.
#(Halusin koittaa single page hommia)

#
# Affirmationin on tarkoitus olla jokin sellainen positiivinen viesti.
#

@app.route('/affirmation/edit/<id>', methods=['GET', 'POST'])
@login_required
def affirmation_edit(id):
    user = g.user
    affirmation = select_affirmation_by_id(id)
    form = AffirmationEditForm(text=affirmation[0][3])

    if form.validate_on_submit():
        update_affirmation_text(id, form.text.data)
        flash('Updated affirmation!')
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/affirmation/edit.html', user=user, form=form, affirmation=affirmation)

@app.route('/affirmation/delete/<id>', methods=['GET', 'POST'])
@login_required
def affirmation_delete(id):
    affirmation = select_affirmation_by_id(id)
    if affirmation == None or affirmation[0][1] != g.user.id:
        flash('Unauthorised enter to affirmation delete.')
        return redirect(url_for('index'))
    delete_affirmation(id)
    flash('Deleted affirmation!')
    return redirect(url_for('main'))