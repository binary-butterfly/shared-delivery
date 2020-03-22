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

import re
import json
import pytz
import math
import decimal
import datetime
from dateutil.parser import parse as dateutil_parse
from urllib.parse import quote_plus
from flask_babel import _


def register_global_filters(app):
    @app.template_filter('commatize')
    def commatize(value):
        output = str(value).replace('.', ',')
        return output

    @app.template_filter('decimal')
    def to_decimal(value):
        if not value:
            return 0
        return decimal.Decimal(value)

    @app.template_filter('beautifuljson')
    def template_beautifiljson(data):
        if not data:
            return ''
        if type(data) == str:
            data = json.loads(data)
        return json.dumps(data, indent=4)

    @app.template_filter('tax')
    def to_decimal(value):
        return str(value * 100).rstrip('0').rstrip('.').replace('.', ',')

    @app.template_filter('jsontolist')
    def json_to_dict(value):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return []

    @app.template_filter('ceil')
    def template_price(value):
        return math.ceil(value)

    @app.template_filter('datetime')
    def template_datetime(value, format='medium'):
        if not value:
            return '...'
        if type(value) == str:
            value = dateutil_parse(value)
        if not value.tzinfo:
            value = pytz.UTC.localize(value).astimezone(pytz.timezone('Europe/Berlin'))
        elif value.tzname() == 'UTC':
            value = value.astimezone(pytz.timezone('Europe/Berlin'))
        if format == 'full':
            strftime_format = "%A, der %d.%m.%y um %H:%M Uhr"
        elif format == 'medium':
            strftime_format = "%d.%m.%y, %H:%M"
        elif format == 'short':
            strftime_format = "%d.%m., %H:%M"
        elif format == 'fulldate':
            strftime_format = "%d.%m.%Y"
        else:
            return '-'
        value = value.strftime(strftime_format)
        return value

    @app.template_filter('date')
    def to_decimal(value):
        if not value:
            return None
        return value.strftime("%d.%m.%Y")

    @app.template_filter('price')
    def template_price(value, digits=2):
        if not value:
            return '0,00 €'
        output = str(round(value, digits)).replace('.', ',')
        if digits == 3 and output[-1] == '0':
            output = output[0:-1]
        return output + ' €'

    @app.template_filter('timedelta')
    def template_timedelta(value, format='medium'):
        result = "%2d" % math.floor(value / 60 / 60)
        if math.floor((value / 60) % 60) or math.floor(value % 60):
            result += ":%02d" % math.floor((value / 60) % 60)
        if math.floor(value % 60):
            result += ":%02d" % math.floor(value % 60)

        if format == 'medium':
            result += ' ' + _('Stunden')
        return result

    @app.template_filter('filter_list')
    def filter_list(list, field, value):
        return [item for item in list if item.get(field) == value]

    @app.context_processor
    def primary_processor():
        def combine_datetime(datetime_from, datetime_till, link=' - ', format='medium'):
            if not datetime_from:
                return '-'
            if type(datetime_from) == str:
                datetime_from = dateutil_parse(datetime_from)
            if not datetime_from.tzinfo:
                datetime_from = pytz.UTC.localize(datetime_from).astimezone(pytz.timezone('Europe/Berlin'))
            elif datetime_from.tzname() == 'UTC':
                datetime_from = datetime_from.astimezone(pytz.timezone('Europe/Berlin'))
            if not datetime_till:
                return template_datetime(datetime_from, format) + link + '...'
            if type(datetime_till) == str:
                datetime_till = dateutil_parse(datetime_till)
            if not datetime_till.tzinfo:
                datetime_till = pytz.UTC.localize(datetime_till).astimezone(pytz.timezone('Europe/Berlin'))
            elif datetime_till.tzname() == 'UTC':
                datetime_till = datetime_till.astimezone(pytz.timezone('Europe/Berlin'))

            if datetime_from.year == datetime_till.year and datetime_from.month == datetime_till.month and datetime_from.day == datetime_till.day:
                strftime_format_day = "%d.%m.%y"
                strftime_format_time = "%H:%M"
                return "%s, %s%s%s" % (
                    datetime_from.strftime(strftime_format_day), datetime_from.strftime(strftime_format_time), link,
                    datetime_till.strftime(strftime_format_time)
                )
            else:
                return template_datetime(datetime_from, format) + link + template_datetime(datetime_till, format)

        return dict(combine_datetime=combine_datetime)

    @app.context_processor
    def inject_now():
        return {'now': datetime.datetime.now()}

    @app.template_filter('urlencode')
    def urlencode(data):
        return (quote_plus(data))
