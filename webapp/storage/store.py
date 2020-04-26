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


class Store(db.Model, BaseModel):
    __tablename__ = 'store'

    fields = [
        'id', 'created', 'modified', 'name', 'firstname', 'lastname', 'company', 'address', 'postalcode', 'locality',
        'country', 'lat', 'lon', 'website', 'email', 'phone', 'mobile', 'fax', 'description', 'website_crowdfunding',
        'website_coupon', 'wheelchair', 'licence', 'brand', 'osm_id', 'revisited_government', 'revisited_store',
        'delivery', 'pickup', 'onlineshop', 'deleted', 'region_id'
    ]

    version = '0.9.0'

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    opening_time = db.relationship('OpeningTime', backref='store', lazy='dynamic')
    #offer = db.relationship('Tag', backref='store', lazy='dynamic')
    #help = db.relationship('Tag', backref='store', lazy='dynamic')

    osm_id = db.Column(db.BigInteger)

    name = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    company = db.Column(db.String(255))
    address = db.Column(db.String(255))
    postalcode = db.Column(db.String(255))
    locality = db.Column(db.String(255))
    country = db.Column(db.String(2))

    lat = db.Column(db.Numeric(precision=8, scale=6), default=0)
    lon = db.Column(db.Numeric(precision=9, scale=6), default=0)

    source_text = db.Column(db.String(255))
    source_url = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)

    website = db.Column(db.String(255))
    website_crowdfunding = db.Column(db.String(255))
    website_coupon = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    fax = db.Column(db.String(255))

    revisited_government = db.Column(db.DateTime)
    revisited_store = db.Column(db.DateTime)
    revisited_user = db.Column(db.DateTime)
    revisited_admin = db.Column(db.DateTime)
    revisited_organisation = db.Column(db.DateTime)

    delivery = db.Column(db.Boolean)
    pickup = db.Column(db.Boolean)
    onlineshop = db.Column(db.Boolean)

    licence = db.Column(db.String(255))
    description = db.Column(db.Text)

    brand = db.Column(db.String(255))
    wheelchair = db.Column(db.Enum('yes', 'limited', 'no', 'designated'))
    organic = db.Column(db.Enum('yes', 'no', 'only'))
    fair_trade = db.Column(db.Enum('yes', 'no', 'only'))
    zero_waste = db.Column(db.Enum('yes', 'no', 'only'))
    _cuisine = db.Column('cuisine', db.Text)
    _origin = db.Column('origin', db.Text)
    _diet = db.Column('diet', db.Text)
    _payment = db.Column('payment', db.Text)

    logo = db.Column(db.Enum('jpg', 'png', 'svg'))
    picture = db.Column(db.Enum('jpg', 'png', 'svg'))

    def to_dict(self, children=False):
        result = super().to_dict()
        if children:
            result['opening-time'] = []
            for opening_time in self.opening_time:
                result['opening-time'].append(opening_time.to_dict())
            result['category'] = []
            for category in self.category:
                result['category'].append(category.to_dict())
            if self.region_id:
                result['region'] = self.region.to_dict()
            else:
                result['region'] = {}

        return result

    def es_index(self, refresh=True):
        from ..store_management.StoreElasticImport import es_index_store
        es_index_store(self, refresh)

    def es_refresh(self):
        from ..store_management.StoreElasticImport import es_refresh_stores
        es_refresh_stores()

    @property
    def revisit_required(self):
        return not (self.revisited_government or self.revisited_store or self.revisited_user or self.revisited_admin or self.revisited_organisation)

    property_out = {
        'yes': 'ja',
        'no': 'nein',
        'limited': 'eingeschänkt',
        'only': 'ausschließlich'
    }

    @property
    def wheelchair_out(self):
        return self.property_out.get(self.wheelchair, self.wheelchair)

    @property
    def organic_out(self):
        return self.property_out.get(self.organic, self.organic)

    @property
    def fair_trade_out(self):
        return self.property_out.get(self.fair_trade, self.fair_trade)

    @property
    def zero_waste_out(self):
        return self.property_out.get(self.zero_waste, self.zero_waste)

    def _get_cuisine(self):
        if not self._cuisine:
            return []
        return json.loads(self._cuisine)

    def _set_cuisine(self, cuisine):
        if cuisine:
            self._cuisine = json.dumps(cuisine)

    cuisine = db.synonym('_cuisine', descriptor=property(_get_cuisine, _set_cuisine))

    def _get_origin(self):
        if not self._origin:
            return []
        return json.loads(self._origin)

    def _set_origin(self, origin):
        if origin:
            self._origin = json.dumps(origin)

    origin = db.synonym('_origin', descriptor=property(_get_origin, _set_origin))

    def _get_diet(self):
        if not self._diet:
            return []
        return json.loads(self._diet)

    def _set_diet(self, diet):
        if diet:
            self._diet = json.dumps(diet)

    diet = db.synonym('_diet', descriptor=property(_get_diet, _set_diet))

    def _get_payment(self):
        if not self._payment:
            return []
        return json.loads(self._payment)

    def _set_payment(self, payment):
        if payment:
            self._payment = json.dumps(payment)

    def logo_url(self, size):
        if not self.logo and size == 'full':
            return '/static/img/store/default.png'
        if not self.logo:
            return '/static/img/store/default.%s.png' % size
        if size == 'full':
            return '/static/img/store/%s.logo.%s' % (self.id, self.logo)
        return '/static/img/store/%s.logo.%s.%s' % (self.id, size, self.logo)

    def picture_url(self, size):
        if not self.picture and size == 'full':
            return '/static/img/store/default.png'
        if not self.picture:
            return '/static/img/store/default.%s.png' % size
        if size == 'full':
            return '/static/img/store/%s.picture.%s' % (self.id, self.picture)
        return '/static/img/store/%s.picture.%s.%s' % (self.id, size, self.picture)

    payment = db.synonym('_payment', descriptor=property(_get_payment, _set_payment))
