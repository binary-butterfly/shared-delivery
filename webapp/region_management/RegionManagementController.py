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


from flask import Blueprint, render_template, flash, redirect, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Region
from .RegionManagementForms import RegionSearchForm, RegionForm, RegionDeleteForm, RegionSyncForm
from ..worker.OsmImport import import_osm_delay
from ..common.file_upload import upload_files

region_management = Blueprint('region_management', __name__, template_folder='templates')

from . import RegionManagementApi


@region_management.route('/admin/regions')
@login_required
def regions_main():
    if not current_user.has_capability('editor'):
        abort(403)
    form = RegionSearchForm()
    return render_template('regions.html', form=form)


@region_management.route('/admin/region/<int:region_id>/show')
@login_required
def region_show(region_id):
    if not current_user.has_capability('editor'):
        abort(403)
    region = Region.query.get_or_404(region_id)
    return render_template('region-show.html', region=region)


@region_management.route('/admin/region/new', methods=['GET', 'POST'])
@login_required
def region_new():
    if not current_user.has_capability('admin'):
        abort(403)
    form = RegionForm()
    if form.validate_on_submit():
        region = Region()
        form.populate_obj(region)
        region.sync_status = 'sync-start'
        db.session.add(region)
        db.session.commit()
        import_osm_delay.delay(region.id)
        upload_files(form, region, 'region')
        flash('Region erfolgreich gespeichert', 'success')
        return redirect('/admin/regions')
    return render_template('region-new.html', form=form)


@region_management.route('/admin/region/<int:region_id>/edit', methods=['GET', 'POST'])
def region_edit(region_id):
    region = Region.query.get_or_404(region_id)
    if not current_user.has_capability('admin') and region not in current_user.region:
        abort(403)
    form = RegionForm(obj=region)
    if form.validate_on_submit():
        form.populate_obj(region)
        db.session.add(region)
        db.session.commit()
        upload_files(form, region, 'region')
        flash('Region erfolgreich gespeichert', 'success')
        return redirect('/admin/regions')
    return render_template('region-edit.html', form=form, region=region)


@region_management.route('/admin/region/<int:region_id>/sync', methods=['GET', 'POST'])
@login_required
def region_sync(region_id):
    if not current_user.has_capability('admin'):
        abort(403)
    region = Region.query.get_or_404(region_id)
    form = RegionSyncForm(obj=region)
    if form.validate_on_submit():
        if form.abort.data:
            return redirect('/admin/regions')
        region.sync_status = 'sync-start'
        db.session.add(region)
        db.session.commit()
        import_osm_delay.delay(region.id)
        flash('Synchronisation erfolgreich gestartet', 'success')
        return redirect('/admin/regions')
    return render_template('region-sync.html', form=form, region=region)

