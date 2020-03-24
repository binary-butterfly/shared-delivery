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

from sqlalchemy import event
from ..extensions import db
from .base import BaseModel
from ..common.helpers import slugify


class Region(db.Model, BaseModel):
    __tablename__ = 'region'

    version = '0.9.1'

    fields = [
        'id', 'created', 'modified', 'name', 'description', 'website', 'lat', 'lon'
    ]

    store = db.relationship('Store', backref='region', lazy='dynamic')

    name = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.Text)

    website = db.Column(db.String(255))

    area = db.Column(db.Text)
    lat = db.Column(db.Numeric(precision=8, scale=6), default=0)
    lon = db.Column(db.Numeric(precision=9, scale=6), default=0)

    logo = db.Column(db.Enum('jpg', 'png'))
    picture = db.Column(db.Enum('jpg', 'png'))


@event.listens_for(Region, 'before_insert')
@event.listens_for(Region, 'before_update')
def update_slug(mapper, connection, region):
    region.slug = slugify(region.name)