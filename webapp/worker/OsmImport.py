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
from urllib.parse import quote
from ..extensions import db, logger
from ..models import Region, Store


def import_osm(region_id):
    region = Region.query.get(region_id)
    if not region:
        return
    sources = {
        'doctors': '[out:json];area[name="%s"];nwr[amenity=doctors](area);out body;',
        'shops': '[out:json];area[name="%s"];nwr[shop=supermarket](area);out body;'
    }
    base_url = 'https://overpass-api.de/api/interpreter?data='

    for slug, param in sources.items():
        result = requests.get(base_url + quote(param % region.name))
        if result.status_code != 200:
            logger.info('bad status code at %s' % slug)
            continue

        for store_raw in result.json().get('elements', []):
            store = Store.query.filter_by(osm_id=store_raw.get('id')).first()
            if not store:
                store = Store()
                store.osm_id = store_raw.get('id')
                store.region_id = region.id
                store.type_slug = slug
            store.name = store_raw.get('tags', {}).get('name')
            if not store.name:
                continue
            store.lat = store_raw.get('lat')
            store.lon = store_raw.get('lon')
            store.address = store_raw.get('tags', {}).get('addr:street', '')
            if store.address and store_raw.get('tags', {}).get('addr:street', ''):
                store.address += ' '
            store.address = store_raw.get('tags', {}).get('addr:housenumber', '')
            store.postalcode = store_raw.get('tags', {}).get('addr:postcode', '')
            store.locality = store_raw.get('tags', {}).get('addr:city', '')
            store.country = 'DE'
            store.brand = store_raw.get('tags', {}).get('brand', '')
            store.wheelchair = store_raw.get('tags', {}).get('wheelchair')
            store.phone = store_raw.get('tags', {}).get('phone')
            if not store.website:
                store.phone = store_raw.get('tags', {}).get('contact:phone')
            store.website = store_raw.get('tags', {}).get('website')
            if not store.website:
                store.website = store_raw.get('tags', {}).get('contact:website')
            db.session.add(store)
            db.session.commit()



        sleep(2)

