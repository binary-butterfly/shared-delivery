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
from flask import request
from flask_login import current_user
from wtforms import DecimalField, StringField, SelectField
from wtforms.utils import unset_value
from decimal import Decimal


class FactorDecimalField(DecimalField):
    def __init__(self, label=None, validators=None, factor=1, **kwargs):
        super(FactorDecimalField, self).__init__(label, validators, **kwargs)
        self.factor = factor

    def process(self, formdata, data=unset_value):
        if data != unset_value and request.method == 'GET':
            if data is None:
                data = 0
            data = Decimal(data) / self.factor
        super(FactorDecimalField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        setattr(obj, name, Decimal(self.data * self.factor))


class TimeStringField(StringField):
    def __init__(self, label=None, validators=None, factor=1, **kwargs):
        super(TimeStringField, self).__init__(label, validators, **kwargs)

    def process(self, formdata, data=unset_value):
        if data != unset_value and request.method == 'GET':
            if data is None:
                data = '0:00:00'
            data = int(data)
            data = "%d:%02d:%02d" % (
                math.floor(data / 60 / 60),
                math.floor((data / 60) % 60),
                math.floor(data % 60)
            )
        super(TimeStringField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        try:
            value = int(self.data[-8:-6]) * 3600 + int(self.data[-5:-3]) * 60 + int(self.data[-2:])
            setattr(obj, name, value)
        except ValueError:
            setattr(obj, name, 0)
