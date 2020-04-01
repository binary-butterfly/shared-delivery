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
from ..models import Category
from .CategoryManagementForms import CategorySearchForm, CategoryForm, CategoryDeleteForm
from ..worker.OsmImport import import_osm_delay
from ..common.file_upload import upload_files

category_management = Blueprint('category_management', __name__, template_folder='templates')

from . import CategoryManagementApi


@category_management.route('/admin/categories')
@login_required
def categorys_main():
    if not current_user.has_capability('editor'):
        abort(403)
    form = CategorySearchForm()
    return render_template('categories.html', form=form)


@category_management.route('/admin/category/<int:category_id>/show')
@login_required
def category_show(category_id):
    if not current_user.has_capability('editor'):
        abort(403)
    category = Category.query.get_or_404(category_id)
    return render_template('category-show.html', category=category)


@category_management.route('/admin/category/new', methods=['GET', 'POST'])
def category_new():
    abort(403)
    if not current_user.has_capability('admin'):
        abort(403)
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        form.populate_obj(category)
        category.sync_status = 'syncing'
        db.session.add(category)
        db.session.commit()
        import_osm_delay.delay(category.id)
        upload_files(form, category, 'category')
        flash('Category erfolgreich gespeichert', 'success')
        return redirect('/admin/categories')
    return render_template('category-new.html', form=form)


@category_management.route('/admin/category/<int:category_id>/edit', methods=['GET', 'POST'])
def category_edit(category_id):
    abort(403)
    if not current_user.has_capability('admin'):
        abort(403)
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        upload_files(form, category, 'category')
        flash('Category erfolgreich gespeichert', 'success')
        return redirect('/admin/categories')
    return render_template('category-edit.html', form=form, category=category)
