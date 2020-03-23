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
from time import sleep
#from urllib.parse import quote
from datetime import datetime
from flask import current_app
from ..extensions import db, logger
from ..models import Region, Store, Category, OpeningTime
from humanized_opening_hours import OHParser


def import_osm(region_id):
    region = Region.query.get(region_id)
    if not region:
        return

    sources = {
        'shop': {
            'bakery': 'Bäckerei',
            'supermarket': 'Supermarkt',
            'pharmacy': 'Apotheke'
        },
        'amenity': {
            'doctors': 'Arztpraxis, Ärztehaus',
            'cafe': 'Café, Eiscafé, Bistro',
            'restaurant': 'Restaurant',
            'pub': 'Kneipe',
            'fast_food': 'Schnell-Restaurant, Imbiss',
            'bar': 'Bar, Nachtlokal'
        }
    }

    for base_key, sub_source in sources.items():
        for category_slug, category_name in sub_source.items():
            import_single_osm(region, base_key, upsert_category(category_slug, category_name))


def upsert_category(category_slug, category_name):
    category = Category.query.filter_by(slug=category_slug).first()
    if not category:
        category = Category()
        category.slug = category_slug
        category.name = category_name
        db.session.add(category)
        db.session.commit()
    return category


def import_single_osm(region, base_key, category):
    url_param = '[out:json];area[name="%s"];nwr[%s=%s](area);out body;' % (
        region.name,
        base_key,
        category.slug
    )
    result = requests.get(current_app.config['OVERPASS_BASE_URL'], {'data': url_param})
    if result.status_code != 200:
        logger.info('bad status code at %s' % category.slug)
        return
    for store_raw in result.json().get('elements', []):
        store = Store.query.filter_by(osm_id=store_raw.get('id')).first()
        if not store:
            store = Store()
            store.osm_id = store_raw.get('id')
            store.region_id = region.id
            store.licence = ''
        elif category not in store.category:
            store.category.append(category)
        store.name = store_raw.get('tags', {}).get('name')
        if not store.name:
            continue
        store.lat = store_raw.get('lat')
        store.lon = store_raw.get('lon')
        store_details = store_raw.get('tags', {})
        store.address = store_details.get('addr:street', '')
        if store.address and store_details.get('addr:street', ''):
            store.address += ' '
        store.address = store_details.get('addr:housenumber', '')
        store.postalcode = store_details.get('addr:postcode', '')
        store.locality = store_details.get('addr:city', '')
        store.country = 'DE'
        store.brand = store_details.get('brand', '')
        store.wheelchair = store_details.get('wheelchair')
        store.phone = store_details.get('phone')
        if not store.website:
            store.phone = store_details.get('contact:phone')
        store.website = store_details.get('website')
        if not store.website:
            store.website = store_details.get('contact:website')
        db.session.add(store)
        db.session.commit()
        save_opening_hours(store.id, store_details.get('opening_hours', ''))
    sleep(2)


def save_opening_hours(store_id, osm_opening_time):
    old_opening_times = []
    opening_times = OpeningTime.query.filter_by(store_id=store_id).all()
    for opening_time in opening_times:
        old_opening_times.append(opening_time.id)
    if osm_opening_time:
        try:
            oh = OHParser(osm_opening_time)
        except:
            if len(old_opening_times):
                OpeningTime.query.filter(OpeningTime.id.in_(old_opening_times)).delete(synchronize_session=False)
            return
        for i in range(0, 7):
            for period in oh.get_day(datetime(2020, 3, 16 + i, 12, 0, 0)).periods:
                begin = period.beginning.time()
                begin_int = begin.hour * 3600 + begin.minute * 60 + begin.second
                end = period.beginning.time()
                end_int = end.hour * 3600 + end.minute * 60 + end.second
                ot = OpeningTime.query\
                    .filter_by(store_id=store_id)\
                    .filter_by(weekday=i+1)\
                    .filter_by(open=begin_int)\
                    .filter_by(close=end_int)\
                    .first()
                if ot:
                    continue
                ot = OpeningTime()
                ot.weekday = i + 1
                ot.type = 'all'
                ot.open = begin_int
                ot.close = end_int
                ot.store_id = store_id
                db.session.add(ot)
    db.session.commit()
    if len(old_opening_times):
        OpeningTime.query.filter(OpeningTime.id.in_(old_opening_times)).delete(synchronize_session=False)
