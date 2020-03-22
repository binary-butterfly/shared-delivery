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

import pytz
import json
from decimal import Decimal
from datetime import datetime
from ..extensions import db
from .base import BaseModel


class Option(db.Model, BaseModel):
    __tablename__ = 'option'

    version = '0.9.0'

    key = db.Column(db.String(128), index=True)
    type = db.Column(db.Enum('string', 'date', 'datetime', 'integer', 'decimal', 'dict', 'list'))
    value = db.Column(db.Text)

    def to_dict(self):
        result = super().to_dict()
        result.update({
            'key': self.key,
            'value': self.value,
        })
        return result

    @classmethod
    def get(cls, key, default=None):
        option = cls.query.filter_by(key=key).first()
        if not option:
            return default
        output = cls.get_output_value(option)
        return output

    @classmethod
    def get_output_value(cls, option):
        if not option:
            return None
        if not option.type or option.type == 'string':
            return option.value
        elif option.type == 'integer':
            return int(option.value)
        elif option.type == 'decimal':
            return Decimal(option.value)
        elif option.type == 'datetime':
            return datetime.strptime(option.value, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.UTC)
        elif option.type == 'date':
            return datetime.strptime(option.value, '%Y-%m-%d').date()
        elif option.type in ['dict', 'list']:
            return json.loads(option.value)

    @classmethod
    def set(cls, key, value, value_type='string'):
        option = cls.query.filter_by(key=key).first()
        if option:
            if value == cls.get_output_value(option) and value_type == option.type:
                return
        else:
            option = cls()
            option.key = key
        option.modified = datetime.utcnow()
        option.type = value_type
        if value_type == 'string':
            option.value = value
        elif value_type == 'decimal' or value_type == 'integer':
            option.value = str(value)
        elif option.type == 'datetime':
            option.value = value.strftime('%Y-%m-%dT%H:%M:%S')
        elif option.type == 'date':
            option.value = value.strftime('%Y-%m-%d')
        elif option.type in ['dict', 'list']:
            option.value = json.dumps(value)
        db.session.add(option)
        db.session.commit()

    @classmethod
    def delete(cls, key):
        option = cls.query.filter_by(key=key).first()
        if not option:
            return
        db.session.delete(option)
        db.session.commit()
