from flask import render_template, flash, redirect, url_for, g
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import GoalAddForm, GoalEditForm, flash_errors
from app.goals import *

@app.route('/goal_edit/<id>', methods=['GET', 'POST'])
@login_required
def goal_edit(id):
    user = g.user
    goal = select_goal_by_id(id)

    #Pitaisi estaa sopimatonta kaytosta
    if goal == None or goal[0][1] != g.user.id:
        flash('Note not found.')
        return redirect(url_for('index'))

    form = GoalEditForm(isActive=goal[0][4], text=goal[0][2])
    if form.validate_on_submit():
        if (form.isActive.data == goal[0][4]):
            update_goal_text(goal[0][0], form.text.data)
        else:
            if (form.isActive.data):
                update_goal_active(goal[0][0])
            else:
                update_goal_deactivate(goal[0][0])
            update_goal_text(goal[0][0], form.text.data)
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/goal/edit.html', user=user, goal=goal, form=form)

@app.route('/goal_add/', methods=['GET', 'POST'])
@login_required
def goal_add():
    user = g.user
    form = GoalAddForm()
    if form.validate_on_submit():
        if (form.end_date.data is None or form.end_date.data == ""):
            insert_goal(g.user.id,form.text.data,None)
        else:
            #End timen tallentaminen
            #Talla hetkella end_time ei tallennu ja sita ei kayteta
            insert_goal(g.user.id, form.text.data, None)
        return redirect(url_for('main'))
    flash_errors(form)
    return render_template('/goal/add.html', user=user, form=form)

@app.route('/goal/delete/<id>', methods=['GET', 'POST'])
@login_required
def goal_delete(id):
    goal = select_goal_by_id(id)
    if goal == None or goal[0][1] != g.user.id:
        flash('Unauthorised enter to user delete.')
        return redirect(url_for('index'))
    delete_goal(goal[0][0])
    flash("Succesfully deleted goal.")
    return redirect(url_for('main'))