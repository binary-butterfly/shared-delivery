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

import requests
from ..extensions import celery, logger
from ..models import Store, ObjectDump, OpeningTime
from ..extensions import db


@celery.task
def geocode_store_delay(region_id):
    store = Store.query.get(region_id)
    if store.lat and store.lon:
        return
    geocode_store(store)


def geocode_store(store):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'format': 'json',
        'q': '%s, %s %s, Deutschland' % (store.address, store.postalcode, store.name)
    }
    r = requests.get(base_url, params)
    if r.status_code != 200:
        logger.error('region.geocode', 'geocoding region %s failed with http %s' % (store.name, r.status_code))
        return
    data = r.json()
    if not len(data):
        logger.error('region.geocode', 'geocoding region %s failed with no result' % store.name)
        return
    data = data[0]
    if not data.get('lat') or not data.get('lon'):
        logger.error('region.geocode', 'geocoding region %s failed with no lat/lon' % store.name)
    store.lat = data['lat']
    store.lon = data['lon']
    db.session.add(store)
    db.session.commit()


@celery.task
def create_store_revision_delay(store_id):
    store = Store.query.get(store_id)
    if not store:
        return
    create_store_revision(store)


def create_store_revision(store):
    object_dump = ObjectDump()
    object_dump.object_id = store.id
    object_dump.region_id = store.region_id
    object_dump.object = 'store'
    object_dump.type = 'revision'
    object_dump.data = store.to_dict(children=True)
    db.session.add(object_dump)
    db.session.commit()


def get_opening_times_for_form(store_id):
    opening_times = []
    opening_times_db = OpeningTime.query\
        .filter_by(store_id=store_id)\
        .order_by(OpeningTime.weekday, OpeningTime.open)\
        .all()
    for opening_time_db in opening_times_db:
        ot = opening_time_db.to_dict()
        ot['open'] = opening_time_db.open_out
        ot['close'] = opening_time_db.close_out
        opening_times.append(ot)
    return opening_times


def save_opening_times_form(form, opening_times_data, store):
    status = {}
    opening_times = {}
    for field in ['all', 'delivery', 'pickup']:
        status[field] = getattr(form, '%s_switch' % field)
        opening_times[field] = []
        for opening_time in opening_times_data[field]:
            opening_times[field].append({
                'weekday': int(opening_time.weekday.data),
                'open': opening_time.open.data_out,
                'close': opening_time.close.data_out
            })
    save_opening_times(status, opening_times, store)


def save_opening_times(status, opening_times,  store):
    old_ids = []
    for opening_time in store.opening_time:
        old_ids.append(opening_time.id)
    for field in ['all', 'delivery', 'pickup']:
        if status.get(field):
            for opening_time in opening_times[field]:
                opening_time_id = upsert_opening_time(store, opening_time, field)
                if opening_time_id in old_ids:
                    old_ids.remove(opening_time_id)
    if len(old_ids) == 0:
        return
    OpeningTime.query.filter(OpeningTime.id.in_(old_ids)).delete(synchronize_session=False)
    db.session.commit()


def upsert_opening_time(store, opening_time_raw, type):
    for opening_time in store.opening_time:
        if opening_time.weekday != opening_time_raw['weekday']:
            continue
        if opening_time.open != opening_time_raw['open']:
            continue
        if opening_time.close != opening_time_raw['close']:
            continue
        return opening_time.id
    opening_time = OpeningTime()
    opening_time.type = type
    opening_time.weekday = opening_time_raw['weekday']
    opening_time.open = opening_time_raw['open']
    opening_time.close = opening_time_raw['close']
    opening_time.store_id = store.id
    db.session.add(opening_time)
    db.session.commit()
    return opening_time.id
