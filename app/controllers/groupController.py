from flask import render_template, flash, redirect, url_for, g, request
from app import app
from flask_login import login_required
from datetime import datetime

#models
from app.forms import flash_errors, GroupAddForm, DiscussionAddForm
from app.discussions import *
from app.groups import *
from app.users import *

#Grouppien paakontrolleri: sis. edit, add, delete ja listaus

#Tarkistaa tietokannasta onko tama kaytttaja taman ryhman admin (tarvitaan sivulogiikassa)
def is_user_admin(user_id, group_id):
    isA = is_user_group_admin(user_id, group_id)
    if (isA[0][0] == 1):
        return True
    else:
        return False

#Tarkistaa tietokannasta onko tama kayttaja tassa ryhmassa
def is_user_in_this_group(user_id, group_id):
    isU = is_user_in_group(user_id, group_id)
    if (isU[0][0] == 1):
        return True
    else:
        return False

#Kaikkien ryhmien listaussivu
@app.route('/groups')
@login_required
def groups():
    user = g.user
    groups = select_all_groups()

    return render_template('/group/all.html', groups=groups, user=user)

#Omien ryhmien listausisuv
@app.route('/own_groups')
@login_required
def own_groups():
    user = g.user
    groups = select_groups_by_user_id(g.user.id)

    return render_template('/group/all.html', groups=groups, user=user)

#Ryhmien lisays
@app.route('/group_add', methods=['GET', 'POST'])
@login_required
def group_add():
    user = g.user
    form=GroupAddForm()
    if form.validate_on_submit():

        check = select_group_by_name(form.name.data)
        if check != None:  # tarkista onko jo ryhma jolla on tama nimi koska nimi == UNIQUE
            flash('Group name already exists')
            return render_template('/group/add.html', user=user, form=form)

        group_id = insert_group(form.name.data, form.description.data)
        insert_user_in_group_admin(g.user.id, group_id)
        flash("New group created!")
        return redirect(url_for('main'))
    return render_template('/group/add.html', user=user, form=form)

#Ryhman paasivu
@app.route('/group/<id>', methods=['GET', 'POST'])
@login_required
def group(id):
    user= select_by_id_user(g.user.id)
    group = select_group_by_id(id)
    users = select_users_by_group_id(id)
    grouped = is_user_in_this_group(user.id, id)
    admin = is_user_admin(user.id, id)
    discussions = select_discussion_by_group_id(id)
    discussions.reverse()
    form = DiscussionAddForm()
    group_admins = select_group_admins(id)
    admins = []
    for a in group_admins:
        admins.append(a[0])

    #join button, eli ryhmaan liittyminen kun saadaan requestista post 'join' asialta (kuten paasivu):
    if request.method == 'POST':
        j = request.form.getlist('join')
        if (len(j)>0):
            insert_user_in_group(g.user.id, id)
            flash('Joined group!')
            return redirect(url_for('group', id=id))

    #post submit, eli Keskustelun luominen ryhmaan
    if form.validate_on_submit():
        insert_discussion(user.id,id,form.title.data,form.text.data)
        return redirect(url_for('group', id=id))

    return render_template('/group/inspect.html', user=user, group=group, grouped=grouped, users=users, admin=admin, discussions=discussions, form=form, admins=admins)

#Ryhman muokkaus
@app.route('/group/edit/<id>', methods=['GET', 'POST'])
@login_required
def group_edit(id):
    user=g.user
    group = select_group_by_id(id)
    form=GroupAddForm(name=group[0][1], description=group[0][2])

    #Ei admin joka yrittaa paasta sivulle ohjataan pois.
    if not is_user_admin(user.id, id):
        flash('Not allowed.')
        return redirect(url_for('groups'))

    if form.validate_on_submit():
        update_group(form.name.data, form.description.data, id)
        flash("Edited group details!")
        return redirect(url_for('group', id=id))

    flash_errors(form)
    return render_template('/group/edit.html', user=user, group=group, form=form)

#Ryhmasta lahteminen
@app.route('/group/leave/<id>')
@login_required
def leave_group(id):
    user = g.user
    delete_user_in_group(user.id, id)
    flash('Left group!')
    return redirect(url_for('main'))

#tee kayttajasta admin
@app.route('/group/admin/<user_id><group_id>')
@login_required
def make_user_admin(user_id, group_id):
    if is_user_admin(g.user.id, group_id):
        update_group_user_to_admin(user_id, group_id)
        flash('Made user admin!')
    else:
        flash('Not allowed!')
    return redirect(url_for('group', id=group_id))

#poista kayttajan admin
@app.route('/group/admin/demote/<user_id><group_id>')
@login_required
def demote_user_admin(user_id, group_id):
    if is_user_admin(g.user.id, group_id):
        update_group_user_to_not_admin(user_id, group_id)
        flash('Demoted admin!')
    else:
        flash('Not allowed!')
    return redirect(url_for('group', id=group_id))

#kayttajan poisto (adminin toimesta) ryhmasta
@app.route('/group/remove/<user_id><group_id>')
@login_required
def remove_user(user_id, group_id):
    if is_user_admin(g.user.id, group_id):
        delete_user_in_group(user_id, group_id)
        flash('Removed user from group.')
        return redirect(url_for('group', id=group_id))
    else:
        flash('Not allowed.')
        return redirect(url_for('index'))

@app.route('/group/delete/<id>')
@login_required
def group_delete(id):
    if is_user_admin(g.user.id, id):
        flash('Deleted group!')
        delete_group(id)
    else:
        flash('Not allowed.')
    return redirect(url_for('main'))