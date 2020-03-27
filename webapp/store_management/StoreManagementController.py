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

from math import floor
from flask import Blueprint, render_template, flash, redirect, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Store, OpeningTime
from .StoreManagementForms import StoreSearchForm, StoreForm, StoreNewForm, StoreDeleteForm
from webapp.store_management.StoreElasticImport import es_index_store_delay
from webapp.store_management.StoreManagementHelper import create_store_revision_delay, get_opening_times_for_form

store_management = Blueprint('store_management', __name__, template_folder='templates')

from . import StoreManagementApi


@store_management.route('/admin/stores')
@login_required
def stores_main():
    if not current_user.has_capability('admin'):
        abort(403)
    form = StoreSearchForm()
    return render_template('stores.html', form=form)


@store_management.route('/admin/store/<int:store_id>/show', methods=['GET', 'POST'])
@login_required
def store_show(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    store = Store.query.get_or_404(store_id)
    return render_template('store-show.html', store=store)


@store_management.route('/admin/store/new', methods=['GET', 'POST'])
@login_required
def store_new():
    if not current_user.has_capability('admin'):
        abort(403)
    form = StoreForm()
    if form.validate_on_submit():
        store = Store()
        opening_times_data = {}
        for field in ['all', 'delivery', 'pickup']:
            opening_times_data[field] = getattr(form, 'opening_times_%s' % field)
            delattr(form, 'opening_times_%s' % field)
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        save_opening_times(form, opening_times_data, store)
        es_index_store_delay.delay(store.id)
        create_store_revision_delay.delay(store.id)
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-new.html', form=form)


@store_management.route('/admin/store/<int:store_id>/edit', methods=['GET', 'POST'])
@login_required
def store_edit(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    store = Store.query.get_or_404(store_id)

    form = StoreForm(obj=store)
    if form.validate_on_submit():
        opening_times_data = {}
        for field in ['all', 'delivery', 'pickup']:
            opening_times_data[field] = getattr(form, 'opening_times_%s' % field)
            delattr(form, 'opening_times_%s' % field)
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        save_opening_times(form, opening_times_data, store)
        es_index_store_delay.delay(store.id)
        create_store_revision_delay.delay(store.id)
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-edit.html', form=form, store=store, opening_times=get_opening_times_for_form(store.id))


def save_opening_times(form, opening_times_data,  store):
    old_ids = []
    for opening_time in store.opening_time:
        old_ids.append(opening_time.id)
    for field in ['all', 'delivery', 'pickup']:
        if getattr(form, '%s_switch' % field):
            for opening_time in opening_times_data[field]:
                opening_time_id = upsert_opening_time(store, opening_time, field)
                if opening_time_id in old_ids:
                    old_ids.remove(opening_time_id)

    if len(old_ids) == 0:
        return
    OpeningTime.query.filter(OpeningTime.id.in_(old_ids)).delete(synchronize_session=False)
    db.session.commit()


def upsert_opening_time(store, form_opening_time, type):
    for opening_time in store.opening_time:
        if opening_time.weekday != int(form_opening_time.weekday.data):
            continue
        if opening_time.open != form_opening_time.open.data_out:
            continue
        if opening_time.close != form_opening_time.close.data_out:
            continue
        return opening_time.id
    opening_time = OpeningTime()
    opening_time.type = type
    opening_time.weekday = int(form_opening_time.weekday.data)
    opening_time.open = form_opening_time.open.data_out
    opening_time.close = form_opening_time.close.data_out
    opening_time.store_id = store.id
    db.session.add(opening_time)
    db.session.commit()
    return opening_time.id


@store_management.route('/admin/store/<int:store_id>/delete', methods=['GET', 'POST'])
@login_required
def store_delete(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    store = Store.query.get_or_404(store_id)
    form = StoreDeleteForm()
    if form.validate_on_submit():
        if form.abort.data:
            return redirect('/admin/stores')
        store.deleted = True
        db.session.add(store)
        db.session.commit()
        flash('Geschäft erfolgreich gelöscht', 'success')
        return redirect('/admin/stores')
    return render_template('store-delete.html', store=store, form=form)
