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

import json
from flask import current_app, request
from ..common.response import json_response
from ..extensions import csrf, db
from ..models import Store, OpeningTime, ObjectDump
from ..store_frontend.StoreFrontendForm import StoreFrontendForm, OpeningTimeFrontendForm

from .StoreApiController import store_api


@store_api.route('/api/store/<int:store_id>/suggest', methods=['POST'])
@csrf.exempt
def api_store_suggest(store_id):
    try:
        json_data = json.loads(request.data)
    except json.JSONDecodeError:
        return json_response({
            'status': -1,
            'errors': ['invalid json']
        }, cors=True)
    store_check = Store()
    store_check.from_dict(json_data)
    store_form = StoreFrontendForm(obj=store_check)
    if not store_form.validate():
        return json_response({
            'status': -1,
            'errors': store_form.errors
        }, cors=True)
    for opening_time_dict in json_data.get('opening_time'):
        opening_time_check = OpeningTime()
        opening_time_check.from_dict(opening_time_dict)
        opening_time_form = OpeningTimeFrontendForm()
        if not opening_time_form.validate():
            return json_response({
                'status': -1,
                'errors': opening_time_form.errors
            }, cors=True)
    store = Store.query.get(store_id)
    if not store:
        return json_response({
            'status': -1,
            'errors': ['invalid store']
        }, cors=True)
    object_dump = ObjectDump()
    object_dump.data = json_data
    object_dump.type = 'suggestion'
    object_dump.object = 'store'
    object_dump.region_id = store.region_id
    object_dump.object_id = store.id
    db.session.add(object_dump)
    db.session.commit()
    return json_response({
        'status': 0
    }, cors=True)

