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

import json
from decimal import Decimal
from dateutil.parser import parse as dateutil_parse
from ..extensions import db
from ..common.helpers import get_current_time, DefaultJSONEncoder


class BaseModel(object):
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }


    version = '0.9.0'

    fields = ['id']
    fields_decimal = []
    fields_datetime = []
    fields_json = []
    fields_dict = []

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time)

    def to_dict(self):
        return {
            'id': self.id,
            'modified': self.created.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'created': self.created.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'version': self.version
        }

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DefaultJSONEncoder)

    def get_cached(self, obj, value):
        data = json.loads(getattr(self, obj + '_cache'))
        if not value in data:
            return None
        return data[value]

    def load_cache(self, data):
        if type(data) == str:
            data = json.loads(data)
        for field in self.fields:
            if field in self.fields_decimal:
                setattr(self, field, Decimal(data.get(field, 0) if data.get(field, 0) else 0))
            elif field in self.fields_datetime:
                setattr(self, field, dateutil_parse(data.get(field)) if data.get(field) else None)
            elif field in self.fields_json:
                setattr(self, field, json.dumps(data.get(field, {}) if data.get(field, {}) else {}))
            elif field in self.fields_dict:
                setattr(self, field, data.get(field, {}) if data.get(field, {}) else {})
            else:
                setattr(self, field, data.get(field))