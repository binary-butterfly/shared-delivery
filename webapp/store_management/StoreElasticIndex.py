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


import datetime
import elasticsearch
from ..extensions import es
from flask import current_app


def es_create_index():
    index_name = current_app.config['ELASTICSEARCH_STORE_INDEX'] + '-' + datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%s')
    es.indices.create(index=index_name, body={
        'settings': es_settings(),
        'mappings': es_mapping()
    })

    latest_name = current_app.config['ELASTICSEARCH_STORE_INDEX'] + '-latest'
    alias_update = []
    try:
        latest_before = es.indices.get_alias(latest_name).keys()
    except elasticsearch.exceptions.NotFoundError:
        latest_before = []
    for single_before in latest_before:
        alias_update.append({
            'remove': {
                'index': single_before,
                'alias': latest_name
            }
        })
    alias_update.append({
        'add': {
            'index': index_name,
            'alias': latest_name
        }
    })
    es.indices.update_aliases({'actions': alias_update})
    index_before = es.indices.get('%s*' % current_app.config['ELASTICSEARCH_STORE_INDEX'])
    for single_index in index_before:
        if index_name != single_index:
            es.indices.delete(single_index)


def es_mapping():
    return {
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'text'
            },
            'firstname': {
                'type': 'text'
            },
            'lastname': {
                'type': 'text'
            },
            'company': {
                'type': 'text'
            },
            'address': {
                'type': 'text'
            },
            'postalcode': {
                'type': 'text'
            },
            'locality': {
                'type': 'text'
            },
            'country': {
                'type': 'keyword'
            },
            'website': {
                'type': 'keyword'
            },
            'email': {
                'type': 'keyword'
            },
            'phone': {
                'type': 'keyword'
            },
            'mobile': {
                'type': 'keyword'
            },
            'fax': {
                'type': 'keyword'
            },
            'type': {
                'type': 'keyword'
            },
            'description': {
                'type': 'text'
            },
            'tags': {
                'type': 'text'
            },
            'region_id': {
                'type': 'integer'
            },
            'location': {
                'type': 'geo_point'
            },
            'region_name': {
                'type': 'text'
            },
            'region_description': {
                'type': 'text'
            },
            'region_website': {
                'type': 'keyword'
            },
            'lat': {
                'type': 'float'
            },
            'lat': {
                'type': 'lon'
            },
            'region_location': {
                'type': 'geo_point'
            },
            'opening_time': {
                'type': 'nested',
                'properties': {
                    'id': {
                        'type': 'integer'
                    },
                    'open': {
                        'type': 'integer'
                    },
                    'close': {
                        'type': 'integer'
                    },
                    'type': {
                        'type': 'keyword'
                    },
                }
            }
        }
    }


def es_settings():
    return {
        'index': {
            'max_result_window': 65536
        }
    }
