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

import time
import pytz
import datetime
from ..extensions import es
from flask import current_app


class ElasticRequest():

    def __init__(self, index):
        self.start = time.time()
        self.index = index
        self.limit = current_app.config['ITEMS_PER_PAGE']
        self.skip = 0
        self.order_by = '_score'
        self.source = []
        self.datetime_fields = []

        self.aggs = {}
        self.query_parts_must = []
        self.query_parts_filter = []
        self.query_range = {}

        self.result_raw = False

    def add_custom_must(self, custom):
        self.query_parts_must.append(custom)

    def set_q(self, search_string):
        self.query_parts_must.append({
            'query_string': {
                'query': search_string,
                'default_operator': 'and',
            }
        })

    def set_partitial_matches(self, data):
        for key, value in data.items():
            self.set_partitial_match(key, value)

    def set_partitial_match(self, field, match):
        self.query_parts_must.append({
            'regexp': {
                field: '(.*)%s(.*)' % match
            }
        })

    def set_fqs(self, data):
        for key, value in data.items():
            self.set_fq(key, value)

    def set_fq(self, key, value):
        if type(value) == list:
            self.query_parts_filter.append({
                'terms': {
                    key: value
                }
            })
        else:
            self.query_parts_filter.append({
                'term': {
                    key: value
                }
            })

    def set_rqs(self, data):
        for key, values in data.items():
            for operator, value in values.items():
                self.set_range_limit(key, operator, value)

    def set_range_limit(self, key, operator, value):
        if key not in self.query_range:
            self.query_range[key] = {}
        self.query_range[key][operator] = value

    def set_limit(self, limit):
        if limit < 0:
            return
        self.limit = limit

    def set_skip(self, skip):
        if skip < 0:
            return
        self.skip = skip

    def set_order_by(self, order_by):
        self.order_by = order_by

    def set_agg_raw(self, agg_name, agg):
        self.aggs[agg_name] = agg

    def set_agg(self, agg, agg_type='terms'):
        self.aggs[agg] = {
            agg_type: {
                'field': agg
            }
        }

    def set_agg_time(self, agg, time_field, time_interval, time_format):
        self.aggs[agg] = {
            'date_histogram': {
                'field': time_field,
                'interval': time_interval,
                'format': time_format,
                'keyed': True
            }
        }

    def set_agg_time_func(self, agg, time_field, time_interval, time_format, field, func):
        self.set_agg_time(agg, time_field, time_interval, time_format)
        self.aggs[agg]['aggs'] = {
            agg: {
                func: {
                    'field': field
                }
            }
        }

    def set_agg_geo(self, agg, geo_field):
        self.aggs[agg] = {
            'geohash_grid': {
                'field': geo_field,
                'precision': 9
            }
        }

    def set_agg_geo_func(self, agg, geo_field, field, func):
        self.set_agg_geo(agg, geo_field)
        self.aggs[agg]['aggs'] = {
            agg: {
                func: {
                    'field': field
                }
            }
        }

    def generate_query(self):
        for key, value in self.query_range.items():
            self.query_parts_filter.append({
                'range': {
                    key: value
                }
            })

        query = {
            'query': {
                'bool': {}
            }
        }
        if len(self.query_parts_must):
            query['query']['bool']['must'] = self.query_parts_must
        if len(self.query_parts_filter):
            query['query']['bool']['filter'] = self.query_parts_filter
        if self.aggs:
            query['aggs'] = self.aggs
        return query

    def query(self):
        query = self.generate_query()
        self.result_raw = es.search(
            index=self.index,
            body=query,
            sort=self.order_by,
            _source=','.join(self.source),
            size=self.limit,
            from_=self.skip
        )

    def set_localize_datetimes(self, datetimes):
        for datetime in datetimes:
            self.set_localize_datetime(datetime)

    def set_localize_datetime(self, datetime):
        self.datetime_fields.append(datetime)

    def get_results(self):
        if not self.result_raw:
            return False
        result = []
        for item_raw in self.result_raw['hits']['hits']:
            item = item_raw['_source']
            for key in self.datetime_fields:
                if key in item:
                    if item[key]:
                        item[key] = pytz.UTC.localize(datetime.datetime.strptime(item[key], '%Y-%m-%dT%H:%M:%SZ'))\
                            .astimezone(pytz.timezone('Europe/Berlin'))\
                            .strftime('%Y-%m-%dT%H:%M:%S')

            result.append(item)

        return result

    def get_result_count(self):
        if not self.result_raw:
            return False
        return self.result_raw['hits']['total']['value']

    def get_aggs(self):
        result = {}
        for agg in self.aggs.keys():
            if agg in self.result_raw['aggregations'][agg]:
                if 'buckets' in self.result_raw['aggregations'][agg][agg]:
                    result[agg] = self.result_raw['aggregations'][agg][agg]['buckets']
                else:
                    result[agg] = self.result_raw['aggregations'][agg][agg]
            else:
                if 'buckets' in self.result_raw['aggregations'][agg]:
                    result[agg] = self.result_raw['aggregations'][agg]['buckets']
                else:
                    result[agg] = self.result_raw['aggregations'][agg]
        return result
