# encoding: utf-8

"""
Copyright (c) 2012 - 2016, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask_script import Manager
from flask import current_app
from webapp import launch
from webapp.extensions import db
import webapp.models as Models
from flask_migrate import Migrate, MigrateCommand

from webapp.common.prepare_unittest import prepare_unittest as prepare_unittest_run
from webapp.store_management.StoreElasticImport import es_create_index as es_create_index_run
from webapp.worker.OsmImport import import_osm as import_osm_run
from webapp.worker.OsmImport import sync_all_regions as sync_all_regions_run
from webapp.store_management.StoreElasticImport import es_index_stores as es_index_stores_run


app = launch()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=current_app, db=db, models=Models)


@manager.command
def prepare_unittest():
    prepare_unittest_run()


@manager.command
def es_create_index():
    es_create_index_run()


@manager.command
def es_index_stores():
    es_index_stores_run()


@manager.command
def sync_all_regions():
    sync_all_regions_run()


@manager.command
def import_osm(region_id):
    import_osm_run(region_id)


if __name__ == "__main__":
    manager.run()
