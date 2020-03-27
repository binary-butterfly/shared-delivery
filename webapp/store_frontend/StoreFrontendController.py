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

from ..models import Store, OpeningTime, ObjectDump
from ..extensions import db
from .StoreFrontendForm import StoreFrontendForm
from ..store_management.StoreManagementHelper import get_opening_times_for_form, create_store_revision

store_frontend = Blueprint('store_frontend', __name__, template_folder='templates')


@store_frontend.route('/store/<int:store_id>')
def store_frontend_main(store_id):
    store = Store.query.get_or_404(store_id)
    opening_times = OpeningTime.query.filter_by(store_id=store.id).order_by(OpeningTime.weekday, OpeningTime.open).all()
    return render_template('store-frontend.html', store=store, opening_times=opening_times)


@store_frontend.route('/store/<int:store_id>/suggest', methods=['GET', 'POST'])
def store_frontend_suggest(store_id):
    store = Store.query.get_or_404(store_id)
    form = StoreFrontendForm(obj=store)
    if form.validate_on_submit():
        opening_times_data = {}
        for field in ['all', 'delivery', 'pickup']:
            opening_times_data[field] = getattr(form, 'opening_times_%s' % field)
            delattr(form, 'opening_times_%s' % field)
        form.populate_obj(store)
        store_suggestion = store.to_dict()
        store_suggestion['opening_time'] = []
        for field in ['all', 'delivery', 'pickup']:
            if getattr(form, '%s_switch' % field):
                for opening_time in opening_times_data[field]:
                    store_suggestion['opening_time'].append({
                        'weekday': opening_time.weekday.data,
                        'open': opening_time.open.data_out,
                        'close': opening_time.close.data_out
                    })
        store_suggestion['category'] = form.category.data
        object_dump = ObjectDump()
        object_dump.data = store_suggestion
        object_dump.type = 'suggestion'
        object_dump.object = 'store'
        object_dump.region_id = store.region_id
        object_dump.object_id = store.id
        db.session.add(object_dump)
        db.session.commit()
        flash('Danke für Deinen Verbesserungsvorschlag!', 'success')
        return redirect('/store/%s' % store.id)
    return render_template('store-suggest.html', store=store, opening_times=get_opening_times_for_form(store.id), form=form)

