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

from flask import current_app
from flask_login import login_required

from ..common.response import json_response
from ..models import Category

from .CategoryManagementForms import CategorySearchForm
from .CategoryManagementController import category_management


@category_management.route('/api/admin/categories', methods=['POST'])
@login_required
def api_categorys():
    data = []

    form = CategorySearchForm()
    if not form.validate_on_submit():
        return json_response({
            'status': -1,
            'errors': form.errors
        })
    categorys = Category.query
    if form.name.data:
        categorys = categorys.filter(Category.name.like('%%%s%%' % form.name.data))

    count = categorys.count()
    categorys = categorys.order_by(getattr(getattr(Category, form.sort_field.data), form.sort_order.data)())\
        .limit(current_app.config['ITEMS_PER_PAGE'])\
        .offset((form.page.data - 1) * current_app.config['ITEMS_PER_PAGE'])\
        .all()
    for category in categorys:
        item = category.to_dict()
        data.append(item)
    return json_response({
        'data': data,
        'status': 0,
        'count': count
    })


