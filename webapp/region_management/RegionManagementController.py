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


from flask import Blueprint, render_template, flash, redirect
from flask_login import login_required

from ..extensions import db
from ..models import Region
from .RegionManagementForms import RegionSearchForm, RegionForm, RegionDeleteForm

region_management = Blueprint('region_management', __name__, template_folder='templates')

from . import RegionManagementApi


@region_management.route('/admin/regions')
@login_required
def regions_main():
    form = RegionSearchForm()
    return render_template('regions.html', form=form)


@region_management.route('/admin/region/new', methods=['GET', 'POST'])
@login_required
def region_new():
    form = RegionForm()
    if form.validate_on_submit():
        region = Region()
        form.populate_obj(region)
        db.session.add(region)
        db.session.commit()
        flash('Region erfolgreich gespeichert', 'success')
        return redirect('/admin/regions')
    return render_template('region-new.html', form=form)


@region_management.route('/admin/region/<int:region_id>/edit', methods=['GET', 'POST'])
@login_required
def region_edit(region_id):
    region = Region.query.get_or_404(region_id)
    form = RegionForm(obj=region)
    if form.validate_on_submit():
        form.populate_obj(region)
        db.session.add(region)
        db.session.commit()
        flash('Region erfolgreich gespeichert', 'success')
        return redirect('/admin/regions')
    return render_template('region-edit.html', form=form, region=region)
