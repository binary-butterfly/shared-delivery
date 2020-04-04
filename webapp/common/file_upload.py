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

import os
from PIL import Image
from flask import current_app, request
from ..extensions import db


def upload_files(form, obj, obj_type):
    if form.logo.data and request.files.get('logo'):
        ending = mimetype_deref[request.files.get('logo').content_type]
        form.logo.data.save(
            os.path.join(current_app.config['IMG_DIR'], obj_type, '%s.logo.%s' % (obj.id, ending))
        )
        if ending != 'svg':
            create_thumbnail(os.path.join(current_app.config['IMG_DIR'], obj_type, '%s.logo.%s' % (obj.id, ending)))
        obj.logo = ending
        db.session.add(obj)

    if form.picture.data and request.files.get('picture'):
        ending = mimetype_deref[request.files.get('picture').content_type]
        form.picture.data.save(
            os.path.join(current_app.config['IMG_DIR'], obj_type, '%s.picture.%s' % (obj.id, ending))
        )
        if ending != 'svg':
            create_thumbnail(os.path.join(current_app.config['IMG_DIR'], obj_type, '%s.picture.%s' % (obj.id, ending)))
        obj.picture = ending

    if form.logo.data or form.picture.data:
        db.session.add(obj)
        db.session.commit()


mimetype_deref = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/svg+xml': 'svg',
    'image/gif': 'gif'
}


def create_thumbnail(path_png):
    file_path, ext = os.path.splitext(path_png)
    image = Image.open(path_png)
    for thumbnail_size in current_app.config['THUMBNAIL_SIZES']:
        image.thumbnail(thumbnail_size)
        image.save(file_path + '.%s.png' % thumbnail_size[0])

