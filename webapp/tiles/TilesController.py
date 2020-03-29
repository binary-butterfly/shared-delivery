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

from sqlalchemy import or_, not_
from flask import Blueprint, render_template, abort

from ..models import Region, Category, Store, OpeningTime

tiles = Blueprint('tiles', __name__, template_folder='templates')


@tiles.route('/')
def regions_main():
    regions = Region.query.order_by(Region.name).all()
    return render_template('frontpage.html', regions=regions)


@tiles.route('/region/<string:region_slug>')
def regions_categories(region_slug):
    region = Region.query.filter_by(slug=region_slug).first()
    if not region:
        abort(404)
    categories = Category.query\
        .filter(Category.store.any())\
        .order_by(Category.priority.asc(), Category.name.asc()).all()
    return render_template('region.html', region=region, categories=categories)


@tiles.route('/region/<string:region_slug>/<string:category_slug>')
def regions_stores(region_slug, category_slug):
    region = Region.query.filter_by(slug=region_slug).first()
    category = Category.query.filter_by(slug=category_slug).first()
    if not region or not category:
        abort(404)
    stores = Store.query\
        .filter_by(deleted=False)\
        .filter(or_(Store.revisited_government != None, Store.revisited_user != None, Store.revisited_store != None, Store.revisited_admin != None))\
        .filter_by(region_id=region.id) \
        .filter(Store.category.contains(category)) \
        .order_by(Store.name.asc()).all()

    stores_help = Store.query\
        .filter_by(deleted=False) \
        .filter(not_(or_(Store.revisited_government != None, Store.revisited_user != None, Store.revisited_store != None, Store.revisited_admin != None))) \
        .filter_by(region_id=region.id) \
        .filter(Store.category.contains(category)) \
        .order_by(Store.name.asc()).all()
    return render_template('store-list.html', region=region, category=category, stores=stores, stores_help=stores_help)

