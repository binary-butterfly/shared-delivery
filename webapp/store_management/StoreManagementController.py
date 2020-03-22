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


from flask import Blueprint, render_template, flash, redirect
from flask_login import login_required

from ..extensions import db
from ..models import Store
from .StoreManagementForms import StoreSearchForm, StoreForm, StoreDeleteForm
from webapp.store_management.StoreElasticImport import es_index_store_delay
from webapp.store_management.StoreManagementHelper import create_store_revision

store_management = Blueprint('store_management', __name__, template_folder='templates')

from . import StoreManagementApi


@store_management.route('/admin/stores')
@login_required
def stores_main():
    form = StoreSearchForm()
    return render_template('stores.html', form=form)


@store_management.route('/admin/store/new', methods=['GET', 'POST'])
@login_required
def store_new():
    form = StoreForm()
    if form.validate_on_submit():
        store = Store()
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        es_index_store_delay.delay(store.id)
        create_store_revision.delay(store.id)
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-new.html', form=form)


@store_management.route('/admin/store/<int:store_id>/edit', methods=['GET', 'POST'])
@login_required
def store_edit(store_id):
    store = Store.query.get_or_404(store_id)
    form = StoreForm(obj=store)
    if form.validate_on_submit():
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        es_index_store_delay.delay(store.id)
        create_store_revision.delay(store.id)
        flash('Geschäft erfolgreich gespeichert', 'success')
        return redirect('/admin/stores')
    return render_template('store-edit.html', form=form, store=store)
