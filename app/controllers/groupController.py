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

def is_user_admin(user_id, group_id):
    isA = is_user_group_admin(user_id, group_id)
    if (isA[0][0] == 1):
        return True
    else:
        return False

def is_user_in_this_group(user_id, group_id):
    isU = is_user_in_group(user_id, group_id)
    if (isU[0][0] == 1):
        return True
    else:
        return False

@app.route('/group/<id>', methods=['GET', 'POST'])
@login_required
def group(id):
    user=g.user
    group = select_group_by_id(id)
    users = select_users_by_group_id(id)
    grouped = is_user_in_this_group(user.id, id)
    admin = is_user_admin(user.id, id)

    if request.method == 'POST':
        j = request.form.getlist('join')
        if (len(j)>0):
            insert_user_in_group(g.user.id, id)
            return redirect(url_for('group', id=id))
    return render_template('/group/inspect.html', user=user, group=group, grouped=grouped, users=users, admin=admin)

@app.route('/group/edit/<id>', methods=['GET', 'POST'])
@login_required
def group_edit(id):
    user=g.user
    group = select_group_by_id(id)
    form=GroupAddForm(name=group[0][1], description=group[0][2])

    if not is_user_admin(user.id, id):
        flash('No.')
        return redirect(url_for('groups'))

    if form.validate_on_submit():
        update_group(form.name.data, form.description.data, id)
        flash("Edited group details!")
        return redirect(url_for('group', id=id))

    flash_errors(form)
    return render_template('/group/edit.html', user=user, group=group, form=form)

@app.route('/group/leave/<id>')
@login_required
def leave_group(id):
    user = g.user
    delete_user_in_group(user.id, id)
    flash('Left group!')
    return redirect(url_for('main'))

@app.route('/group/remove/<user_id><group_id>')
@login_required
def remove_user(user_id, group_id):
    if is_user_admin(g.user.id, group_id):
        delete_user_in_group(user_id, group_id)
        flash('Removed user from group.')
        return redirect(url_for('group', id=group_id))
    else:
        flash('Not allowed.')
        return redirect(url_for('main'))

@app.route('/group/delete/<id>')
@login_required
def group_delete(id):
    if is_user_admin(g.user.id, id):
        flash('Deleted group!')
        delete_group(id)
    else:
        flash('Not allowed.')
    return redirect(url_for('main'))