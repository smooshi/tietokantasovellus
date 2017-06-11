from flask import render_template, flash, redirect, url_for, g, request
from app import app
from flask_login import login_required

#models
from app.forms import flash_errors, DiscussionAddForm
from app.discussions import *
from app.groups import *

#onko kayttaja ryhman admin
def is_user_admin(user_id, group_id):
    isA = is_user_group_admin(user_id, group_id)
    if (isA[0][0] == 1):
        return True
    else:
        return False

@app.route('/discussion_edit/<id>', methods=['GET', 'POST'])
@login_required
def discussion_edit(id):
    user = g.user
    discussion = select_discussion_by_id(id)
    if discussion == None or discussion[0][1] != g.user.id:
        flash('Discussion not found.')
        return redirect(url_for('index'))

    form = DiscussionAddForm(title=discussion[0][3], text=discussion[0][4])
    if form.validate_on_submit():
        update_discussion_text(id, form.title.data, form.text.data)
        flash('Succesfully edited post.')
        return redirect(url_for('group', id=discussion[0][2]))
    return render_template('/discussions/edit.html', form =form, user=user, discussion=discussion)

@app.route('/discussion_delete/<id>')
@login_required
def discussion_delete(id):
    discussion = select_discussion_by_id(id)
    if discussion == None or discussion[0][1] != g.user.id:
        if is_user_admin(g.user.id, discussion[0][2]):
            flash('Admin deleted discussion')
            delete_discussion(discussion[0][0])
            return redirect(url_for('group', id=discussion[0][2]))
        flash('Unauthorised enter to disucssion delete.')
        return redirect(url_for('index'))
    delete_discussion(discussion[0][0])
    flash("Succesfully deleted discussion.")
    return redirect(url_for('group', id=discussion[0][2]))