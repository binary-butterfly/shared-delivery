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

import math
from datetime import datetime
from ..models import Store, Option
from ..extensions import db, es, celery
from .StoreElasticIndex import es_create_index
from flask import current_app


def es_index_stores(recreate=False):
    """

    """
    sync_start = datetime.utcnow()
    last_sync = Option.get('elasticsearch-store-sync-last', datetime(2010, 1, 1, 0, 0, 0))

    if not es.indices.exists_alias(name=current_app.config['ELASTICSEARCH_STORE_INDEX'] + '-latest') or recreate:
        es_create_index()

    stores = Store.query.filter(Store.delivery_datetime != None)
    if last_sync and not recreate:
        stores = stores.filter(Store.modified >= last_sync)

    for store in stores.all():
        es_index_store(store)

    Option.set('elasticsearch-store-sync-last', sync_start, 'datetime')


@celery.task
def es_index_store_delay(store_id):
    store = Store.query.get(store_id)
    if not store:
        return
    es_index_store(store)


def es_index_store(store):
    index_name = current_app.config['ELASTICSEARCH_STORE_INDEX'] + '-latest'

    store_dict = store.to_dict()
    if store.lat and store.lon:
        store_dict['location'] = '%s,%s' % (store.lat, store.lon)
    es.index(
        index=index_name,
        id='store-%s' % store.id,
        body=store_dict
    )
    es.indices.refresh(index=index_name)
