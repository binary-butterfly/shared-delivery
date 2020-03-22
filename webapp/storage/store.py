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


from ..extensions import db
from .base import BaseModel


class Store(db.Model, BaseModel):
    __tablename__ = 'store'

    fields = [
        'firstname', 'lastname', 'company', 'address', 'postalcode', 'locality', 'country', 'lat', 'lon', 'website',
        'email', 'phone', 'mobile', 'fax', 'type', 'description'
    ]

    version = '0.9.0'

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    opening_time = db.relationship('OpeningTime', backref='store', lazy='dynamic')
    #offer = db.relationship('Tag', backref='store', lazy='dynamic')
    #help = db.relationship('Tag', backref='store', lazy='dynamic')

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

    website = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    fax = db.Column(db.String(255))

    type = db.Column(db.String(255))

    description = db.Column(db.Text)

    def to_dict(self):
        result = super().to_dict()
        for field in self.fields:
            result[field] = getattr(self, field)
        return result

