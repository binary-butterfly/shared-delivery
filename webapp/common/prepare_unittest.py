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

import pymysql
from urllib.parse import urlparse
from flask import current_app
from ..common.helpers import send_json
from ..models import User
from ..extensions import db


def prepare_unittest():
    if current_app.config['MODE'] != 'DEVELOPMENT' or not current_app.config['DEBUG']:
        print('wrong mode')
        return

    url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])
    connection = pymysql.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        db=url.path[1:],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        for line in truncate_dbs.split("\n"):
            if not line:
                continue
            cursor.execute(line)
    connection.commit()

    user = User()
    user.email = 'mail@ernestoruge.de'
    user.password = 'unittest'
    user.first_name = 'Ernesto'
    user.last_name = 'Ruge'
    user.company = 'binary butterfly GmbH'
    user.address = 'Am Hertinger Tor'
    user.postalcode = '59423'
    user.locality = 'Unna'
    user.country = 'DE'
    user.status = 'active'
    user.capabilities = ['admin']
    db.session.add(user)
    db.session.commit()


truncate_dbs = '''
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE `option`;
TRUNCATE `user`;
SET FOREIGN_KEY_CHECKS=1;
'''
