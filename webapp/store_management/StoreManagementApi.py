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

from sqlalchemy import or_, not_
from flask import current_app, abort
from flask_login import current_user

from ..common.response import json_response
from ..models import Store, ObjectDump

from .StoreManagementForms import StoreSearchForm, StoreSuggestionSearchForm
from .StoreManagementController import store_management


@store_management.route('/api/admin/stores', methods=['POST'])
def api_stores():
    if not current_user.has_capability('editor'):
        abort(403)
    data = []

    form = StoreSearchForm()
    if not form.validate_on_submit():
        return json_response({
            'status': -1,
            'errors': form.errors
        })
    stores = Store.query.filter(Store.deleted == False)
    if form.name.data:
        stores = stores.filter(Store.name.like('%%%s%%' % form.name.data))

    if form.region.data and form.region.data not in ['None', '_all']:
        stores = stores.filter_by(region_id=form.region.data)
    elif not current_user.has_capability('admin'):
        stores = stores.filter(Store.region_id.in_(current_user.region_ids))

    if form.revisit_required.data and form.revisit_required.data not in ['None', '_all']:
        if form.revisit_required.data == 'yes':
            stores = stores.filter(not_(or_(Store.revisited_government != None, Store.revisited_user != None, Store.revisited_store != None, Store.revisited_admin != None)))
        else:
            stores = stores.filter(or_(Store.revisited_government != None, Store.revisited_user != None, Store.revisited_store != None, Store.revisited_admin != None))

    count = stores.count()
    stores = stores.order_by(getattr(getattr(Store, form.sort_field.data), form.sort_order.data)())\
        .limit(current_app.config['ITEMS_PER_PAGE'])\
        .offset((form.page.data - 1) * current_app.config['ITEMS_PER_PAGE'])\
        .all()
    for store in stores:
        item = store.to_dict()
        data.append(item)
    return json_response({
        'data': data,
        'status': 0,
        'count': count
    })


@store_management.route('/api/admin/store/suggestions', methods=['POST'])
def api_store_suggestions():
    if not current_user.has_capability('editor'):
        abort(403)
    data = []

    form = StoreSuggestionSearchForm()
    if not form.validate_on_submit():
        return json_response({
            'status': -1,
            'errors': form.errors
        })
    stores = ObjectDump.query.filter_by(type='suggestion')

    if form.region.data and form.region.data not in ['None', '_all']:
        stores = stores.filter_by(region_id=form.region.data)
    elif not current_user.has_capability('admin'):
        stores = stores.filter(Store.region_id.in_(current_user.region_ids))

    if form.settled.data and form.settled.data not in ['None', '_all']:
        stores = stores.filter_by(settled=form.settled.data == 'yes')

    count = stores.count()
    stores = stores.order_by(getattr(getattr(ObjectDump, form.sort_field.data), form.sort_order.data)())\
        .limit(current_app.config['ITEMS_PER_PAGE'])\
        .offset((form.page.data - 1) * current_app.config['ITEMS_PER_PAGE'])\
        .all()
    for store in stores:
        item = store.data
        item['id'] = store.id
        item['created'] = store.created
        data.append(item)
    return json_response({
        'data': data,
        'status': 0,
        'count': count
    })
