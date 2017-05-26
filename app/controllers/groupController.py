from flask import render_template, flash, redirect, url_for, g, request
from app import app
from flask_login import login_required

#models
from app.forms import flash_errors, GroupAddForm
from app.models import *
from app.groups import *

@app.route('/groups')
@login_required
def groups():
    user = g.user
    groups = select_all_groups()
    return render_template('/group/all.html', groups=groups, user=user)

@app.route('/own_groups')
@login_required
def own_groups():
    user = g.user
    groups = select_groups_by_user_id(g.user.id)
    #u_i_g = select_this_users_groups(g.user.id)
    #gr = list()
    #for user_id, group_id, isAdmin in u_i_g:
    #    gr.append(select_group_by_id(group_id))
    #groups = list()
    #for group in gr:
    #    for id, name, description, created_at, edited_at in group:
    #        groups.append((id,name,description,created_at,edited_at))

    return render_template('/group/all.html', groups=groups, user=user)

@app.route('/group_add', methods=['GET', 'POST'])
@login_required
def group_add():
    user = g.user
    form=GroupAddForm()
    if form.validate_on_submit():
        group_id = insert_group(form.name.data, form.description.data)
        insert_user_in_group_admin(g.user.id, group_id)
        flash("New group created!")
        return redirect(url_for('main'))
    return render_template('/group/add.html', user=user, form=form)

@app.route('/group/<id>', methods=['GET', 'POST'])
@login_required
def group(id):
    user=g.user
    group = select_group_by_id(id)
    users = select_users_by_group_id(id)
    grouped = False
    userNames = list()

    #does g.user belong in this group
    isU = is_user_in_group(g.user.id, id)
    if (isU[0][0] == 1):
        grouped = True
        for i in range (0, len(users)):
            userNames.append(users[i][2])

    if request.method == 'POST':
        j = request.form.getlist('join')
        if (len(j)>0):
            insert_user_in_group(g.user.id, id)
            return redirect(url_for('group', id=id))
    return render_template('/group/inspect.html', user=user, group=group, grouped=grouped, userNames=userNames)