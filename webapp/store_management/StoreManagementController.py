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

from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Store, OpeningTime, ObjectDump
from .StoreManagementForms import StoreSearchForm, StoreForm, StoreNewForm, StoreDeleteForm, StoreSuggestionSearchForm, \
    StoreSuggestionMergeForm
from webapp.store_management.StoreElasticImport import es_index_store_delay
from webapp.store_management.StoreManagementHelper import create_store_revision_delay, get_opening_times_for_form,\
    save_opening_times, save_opening_times_form
from ..common.file_upload import upload_files

store_management = Blueprint('store_management', __name__, template_folder='templates')

from . import StoreManagementApi


@store_management.route('/admin/stores')
def stores_main():
    if not current_user.has_capability('editor'):
        abort(403)
    form = StoreSearchForm()
    return render_template('stores.html', form=form)


@store_management.route('/admin/store/<int:store_id>/show', methods=['GET', 'POST'])
def store_show(store_id):
    if not current_user.has_capability('editor'):
        abort(403)
    store = Store.query.get_or_404(store_id)
    opening_times = OpeningTime.query.filter_by(store_id=store.id).order_by(OpeningTime.weekday, OpeningTime.open).all()
    return render_template('store-show.html', store=store, opening_times=opening_times)


@store_management.route('/admin/store/new', methods=['GET', 'POST'])
def store_new():
    if not current_user.has_capability('editor'):
        abort(403)
    form = StoreNewForm()
    if form.validate_on_submit():
        store = Store()
        opening_times_data = {}
        for field in ['all', 'delivery', 'pickup']:
            opening_times_data[field] = getattr(form, 'opening_times_%s' % field)
            delattr(form, 'opening_times_%s' % field)
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        save_opening_times_form(form, opening_times_data, store)
        es_index_store_delay.delay(store.id)
        create_store_revision_delay.delay(store.id)
        upload_files(form, store, 'store')
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-new.html', form=form)


@store_management.route('/admin/store/<int:store_id>/edit', methods=['GET', 'POST'])
def store_edit(store_id):
    if not current_user.has_capability('editor'):
        abort(403)
    store = Store.query.get_or_404(store_id)
    if not current_user.has_capability('admin') and store.region not in current_user.region:
        abort(403)
    form = StoreForm(obj=store)
    if form.validate_on_submit():
        opening_times_data = {}
        for field in ['all', 'delivery', 'pickup']:
            opening_times_data[field] = getattr(form, 'opening_times_%s' % field)
            delattr(form, 'opening_times_%s' % field)
        form.populate_obj(store)
        setattr(store, 'revisited_%s' % current_user.role, datetime.utcnow())
        db.session.add(store)
        db.session.commit()
        save_opening_times_form(form, opening_times_data, store)
        es_index_store_delay.delay(store.id)
        create_store_revision_delay.delay(store.id)
        upload_files(form, store, 'store')
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-edit.html', form=form, store=store, opening_times=get_opening_times_for_form(store.id))


@store_management.route('/admin/store/<int:store_id>/delete', methods=['GET', 'POST'])
def store_delete(store_id):
    if not current_user.has_capability('admin'):
        abort(403)
    store = Store.query.get_or_404(store_id)
    if not current_user.has_capability('admin') and store.region not in current_user.region:
        abort(403)
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


@store_management.route('/admin/store/suggestions', methods=['GET', 'POST'])
def store_suggestions():
    if not current_user.has_capability('editor'):
        abort(403)
    form = StoreSuggestionSearchForm()
    return render_template('store-suggestions.html', form=form)


@store_management.route('/admin/store/suggestion/<int:suggestion_id>/show', methods=['GET', 'POST'])
def store_suggestion_show(suggestion_id):
    if not current_user.has_capability('editor'):
        abort(403)
    object_dump = ObjectDump.query.get_or_404(suggestion_id)
    store = Store.query.get_or_404(object_dump.object_id)
    if not current_user.has_capability('admin') and store.region not in current_user.region:
        abort(403)
    suggestion = Store()
    suggestion.load_cache(object_dump.data)
    opening_times_data = {
        'new': [],
        'old': [],
        'both': []
    }
    new_opening_times = object_dump.data.get('opening_time', [])
    opening_times = OpeningTime.query.filter_by(store_id=store.id).order_by(OpeningTime.weekday, OpeningTime.open).all()
    for opening_time in opening_times:
        found = -1
        for i in range(0, len(new_opening_times)):
            if opening_time.weekday != int(new_opening_times[i]['weekday']):
                continue
            if opening_time.open != new_opening_times[i]['open']:
                continue
            if opening_time.close != new_opening_times[i]['close']:
                continue
            found = i
            break
        if found >= 0:
            opening_times_data['both'].append(opening_time)
            del new_opening_times[found]
            continue
        opening_times_data['old'].append(opening_time)
    for new_opening_time in new_opening_times:
        new_opening_time_obj = OpeningTime()
        new_opening_time_obj.load_cache(new_opening_time)
        opening_times_data['new'].append(new_opening_time_obj)
    form = StoreSuggestionMergeForm()
    if form.validate_on_submit():
        if form.abort.data:
            return redirect('/admin/store/suggestions')
        if form.delete.data:
            object_dump.deleted = True
            db.session.add(object_dump)
            db.session.commit()
            flash('Verbesserungsvorschlag wurde erfolgreich gelöscht.', 'success')
            return redirect('/admin/store/suggestions')
        if form.edit.data:
            return redirect('/admin/store/suggestion/%s/edit' % suggestion.id)
        store.load_cache(object_dump.data)
        store.revisited_user = object_dump.created
        db.session.add(store)
        db.session.commit()
        new_opening_times_dict = {'all': [], 'delivery': [], 'pickup': []}
        for new_opening_time in object_dump.data.get('opening_time', []):
            new_opening_times_dict[new_opening_time.get('type', 'all')].append(new_opening_time)
        save_opening_times({'all': True, 'delivery': True, 'pickup': True}, new_opening_times_dict, store)
        object_dump.settled = True
        db.session.add(object_dump)
        db.session.commit()
        flash('Verbesserungsvorschlag wurde erfolgreich gespeichert.', 'success')
        return redirect('/admin/store/suggestions')
    return render_template(
        'store-suggestion-show.html',
        store=store,
        object_dump=object_dump,
        suggestion=suggestion,
        opening_times_data=opening_times_data,
        form=form
    )


@store_management.route('/admin/store/suggestion/<int:suggestion_id>/edit', methods=['GET', 'POST'])
def store_suggestion_edit(suggestion_id):
    if not current_user.has_capability('editor'):
        abort(403)
    object_dump = ObjectDump.query.get_or_404(suggestion_id)
    store = Store.query.get_or_404(object_dump.object_id)
    return render_template(
        'store-suggestion-edit.html',
        object_dump=object_dump,
        store=store
    )
