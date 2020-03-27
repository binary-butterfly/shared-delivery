# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask import current_app, render_template, redirect, flash, abort
from flask_login import current_user, login_required
from .UserManagementForms import UserForm, UserSearchForm
from ..extensions import db
from ..models import User
from ..common.helpers import get_random_password
from flask_babel import _


from .UserController import user
from . import UserManagementApi


@user.route('/admin/users')
def user_index():
    if not current_user.has_capability('admin'):
        abort(403)
    form = UserSearchForm()
    return render_template('users.html', form=form)


@user.route('/admin/store/<int:store_id>/show', methods=['GET', 'POST'])
def user_show(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    user = User.query.get_or_404(store_id)
    return render_template('user-show.html', user=user)


@user.route('/admin/user/new', methods=['GET', 'POST'])
def user_new():
    if not current_user.has_capability('admin'):
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.password = get_random_password()
        user.capabilities = ['admin']
        db.session.add(user)
        db.session.commit()
        flash('Nutzer erfolgreich gespeichert', 'success')
        return redirect('/admin/users')
    return render_template('user-new.html', form=form)


@user.route('/admin/user/<int:store_id>/edit', methods=['GET', 'POST'])
def user_edit(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    user = User.query.get_or_404(store_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('Nutzer erfolgreich gespeichert', 'success')
        return redirect('/admin/users')
    return render_template('user-edit.html', form=form, user=user)


@user.route('/user/data', methods=['GET', 'POST'])
@login_required
def account_nutzerdaten():
    form = UserForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()

        flash(_('Nutzerdaten gespeichert.'), 'success')
        return redirect('/')
    return render_template('userdata.html', form=form)
