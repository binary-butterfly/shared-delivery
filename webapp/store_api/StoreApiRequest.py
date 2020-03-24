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

from flask import current_app, request
from ..common.elastic_request import ElasticRequest


def get_data(limit=None):
    if request.method == 'GET':
        data = request.args
    else:
        data = request.form
    elastic_request = ElasticRequest(current_app.config['ELASTICSEARCH_STORE_INDEX'] + '-latest')

    if data.get('q'):
        elastic_request.query_parts_must.append({
            'bool': {
                'should': [
                    {
                        'query_string': {
                            'fields': ['name'],
                            'query': data.get('q'),
                            'default_operator': 'and',
                            'boost': 50
                        }
                    },
                    {
                        'query_string': {
                            'fields': ['category'],
                            'query': data.get('q'),
                            'default_operator': 'and',
                            'boost': 35
                        }
                    },
                    {
                        'query_string': {
                            'fields': ['description'],
                            'query': data.get('q'),
                            'default_operator': 'and',
                            'boost': 20
                        }
                    }
                ]
            }
        })
    if data.get('lat') and data.get('lon') and data.get('radius'):
        elastic_request.query_parts_must.append({
            "geo_distance": {
                "distance": "%sm" % data.get('radius', type=int),
                "location": {
                    "lat": data.get('lat', type=float),
                    "lon": data.get('lon', type=float)
                }
            }
        })

    if data.get('category'):
        elastic_request.set_fq('category', data.get('category'))
    if data.get('category-slug'):
        elastic_request.set_fq('category_slug', data.get('category-slug'))
    if data.get('region'):
        elastic_request.set_fq('region_name', data.get('region'))
    if data.get('region-slug'):
        elastic_request.set_fq('region_name', data.get('region-slug'))
    if data.get('region-id'):
        elastic_request.set_fq('region_id', data.get('region-id'))

    if limit:
        elastic_request.set_limit(limit)
    else:
        elastic_request.set_limit(current_app.config['ITEMS_PER_API'])
        elastic_request.set_skip(current_app.config['ITEMS_PER_API'] * (data.get('page', 1, type=int) - 1))

    elastic_request.query()
    return elastic_request.get_results(), elastic_request.get_result_count()
