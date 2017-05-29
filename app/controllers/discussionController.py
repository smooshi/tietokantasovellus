from flask import render_template, flash, redirect, url_for, g, request
from app import app
from flask_login import login_required

#models
from app.forms import flash_errors, DiscussionAddForm
from app.discussions import *

@app.route('/discussion_edit/<id>', methods=['GET', 'POST'])
@login_required
def discussion_edit(id):
    user = g.user
    form = DiscussionAddForm()
    discussion = select_discussion_by_id(id)
    if discussion == None or discussion[0][1] != g.user.id:
        flash('Discussion not found.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash('Attempted to edit post')
    return render_template('/discussions/edit.html', form =form, user=user)

@app.route('/discussion_delete/<id>')
@login_required
def discussion_delete(id):
    flash('Attempted to delete discussion!')
    return redirect(url_for('main'))