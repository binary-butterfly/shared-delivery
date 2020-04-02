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

from ..common.response import json_response
from ..extensions import csrf
from ..models import Store, Region, Category

from .StoreApiController import store_api


@store_api.route('/api/region/<string:region_slug_or_id>')
@csrf.exempt
def api_regions_rest(region_slug_or_id):
    if region_slug_or_id.isnumeric():
        region = Region.query.get(region_slug_or_id)
    else:
        region = Region.query.filter_by(slug=region_slug_or_id).first()
    if not region:
        return json_response({
            'status': 404
        })
    return json_response({
        'status': 0,
        'data': region.to_dict()
    }, cors=True)


@store_api.route('/api/category/<string:category_slug_or_id>')
@csrf.exempt
def api_categorys_rest(category_slug_or_id):
    if category_slug_or_id.isnumeric():
        category = Category.query.get(category_slug_or_id)
    else:
        category = Category.query.filter_by(slug=category_slug_or_id).first()
    if not category:
        return json_response({
            'status': 404
        })
    return json_response({
        'status': 0,
        'data': category.to_dict()
    }, cors=True)


@store_api.route('/api/store/<int:store_id>')
@csrf.exempt
def api_stores_rest(store_id):
    store = Store.query.get(store_id)
    if not store:
        return json_response({
            'status': 404
        })
    return json_response({
        'status': 0,
        'data': store.to_dict(children=True)
    }, cors=True)

