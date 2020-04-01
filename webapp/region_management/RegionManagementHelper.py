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
from ..extensions import db, celery, logger
from ..models import Region


@celery.task
def geocode_region_delay(region_id):
    region = Region.query.get(region_id)
    if region.lat and region.lon:
        return
    geocode_region(region)


def geocode_region(region):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'format': 'json',
        'q': '%s, Deutschland' % region.name
    }
    r = requests.get(base_url, params)
    if r.status_code != 200:
        logger.error('region.geocode', 'geocoding region %s failed with http %s' % (region.name, r.status_code))
        return
    data = r.json()
    if not len(data):
        logger.error('region.geocode', 'geocoding region %s failed with no result' % region.name)
        return
    data = data[0]
    if not data.get('lat') or not data.get('lon'):
        logger.error('region.geocode', 'geocoding region %s failed with no lat/lon' % region.name)
    region.lat = data['lat']
    region.lon = data['lon']
    db.session.add(region)
    db.session.commit()
