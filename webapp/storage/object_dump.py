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
from ..extensions import db
from .base import BaseModel
from ..common.helpers import DefaultJSONEncoder


class ObjectDump(db.Model, BaseModel):
    __tablename__ = 'object_dump'

    version = '0.9.0'

    object_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    type = db.Column(db.Enum('suggestion', 'revision'), index=True)
    object = db.Column(db.String(255), index=True)
    settled = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    _data = db.Column('data', db.Text)

    def _get_data(self):
        return json.loads(self._data, )

    def _set_data(self, data):
        self._data = json.dumps(data, sort_keys=True, cls=DefaultJSONEncoder)

    data = db.synonym('_data', descriptor=property(_get_data, _set_data))

