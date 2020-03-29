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
from wtforms import DecimalField, StringField, SelectMultipleField, SelectField, FileField
from wtforms.utils import unset_value
from decimal import Decimal
from ..models import Region, Category


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
                data = '0:00'
            data = int(data)
            data = "%d:%02d" % (
                math.floor(data / 60 / 60),
                math.floor((data / 60) % 60)
            )
        super(TimeStringField, self).process(formdata, data)

    @property
    def data_out(self):
        return int(self.data[:-3]) * 3600 + int(self.data[-2:]) * 60

    def populate_obj(self, obj, name):
        try:
            value = int(self.data[-5:-3]) * 3600 + int(self.data[-2:]) * 60
            setattr(obj, name, value)
        except ValueError:
            setattr(obj, name, 0)


class ExtendedFileField(FileField):
    def populate_obj(self, obj, name):
        setattr(obj, name, None)


class RegionField(SelectField):
    def __init__(self, all_option=False, limit_allowed=False, **kwargs):
        self.simple_validate = getattr(kwargs['_form'], 'simple_validate', False)
        super(RegionField, self).__init__(**kwargs)
        self.choices = [('_all', 'beliebig')] if all_option else [('0', 'bitte wählen')]
        if self.simple_validate:
            return
        regions = Region.query
        if limit_allowed and not current_user.has_capability('admin'):
            regions = regions.filter(Region.user.contains(current_user))

        regions = regions.order_by(Region.name).all()
        for region in regions:
            self.choices.append((str(region.id), region.name))

    def pre_validate(self, form):
        if self.simple_validate:
            return
        super(RegionField, self).pre_validate(form)

    def process(self, formdata, data=unset_value):
        if data != unset_value and request.method == 'GET':
            data = str(data.id)
        super(RegionField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        setattr(obj, '%s_id' % name, int(self.data))


class RegionMultipleField(SelectMultipleField):
    def __init__(self, all_option=False, **kwargs):
        self.simple_validate = getattr(kwargs['_form'], 'simple_validate', False)
        super(RegionMultipleField, self).__init__(**kwargs)
        self.choices = [('_all', 'beliebig')] if all_option else [('0', 'bitte wählen')]
        if self.simple_validate:
            return
        self.regions = Region.query
        self.regions = self.regions.order_by(Region.name).all()
        for region in self.regions:
            self.choices.append((str(region.id), region.name))

    def pre_validate(self, form):
        if self.simple_validate:
            return
        super(RegionMultipleField, self).pre_validate(form)

    def process(self, formdata, data=unset_value):
        if data != unset_value and request.method == 'GET':
            result = []
            for item in data:
                result.append(str(item.id))
            data = result
        super(RegionMultipleField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        result = []
        for item in self.data:
            for region in self.regions:
                if region.id == int(item):
                    result.append(region)
        setattr(obj, '%s' % name, result)


class CategoryField(SelectMultipleField):
    def __init__(self, all_option=False, **kwargs):
        self.simple_validate = getattr(kwargs['_form'], 'simple_validate', False)
        super(CategoryField, self).__init__(**kwargs)
        self.choices = [('_all', 'beliebig')] if all_option else [('0', 'bitte wählen')]
        if self.simple_validate:
            return
        self.categories = Category.query
        self.categories = self.categories.order_by(Category.name).all()
        for category in self.categories:
            self.choices.append((str(category.id), category.name))

    def pre_validate(self, form):
        if self.simple_validate:
            return
        super(CategoryField, self).pre_validate(form)

    def process(self, formdata, data=unset_value):
        if data != unset_value and request.method == 'GET':
            result = []
            for item in data:
                result.append(str(item.id))
            data = result
        super(CategoryField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        result = []
        for item in self.data:
            for category in self.categories:
                if category.id == int(item):
                    result.append(category)
        setattr(obj, '%s' % name, result)
