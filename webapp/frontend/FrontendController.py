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

import time
from flask import Blueprint, current_app, render_template
from ..models import Option
from ..common.response import json_response

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/status')
def status():
    try:
        start = time.time()
        option = Option.get('app-status', 1)
    except:
        return json_response({
            'status': -1
        })
    return json_response({
        'status': 0 if option == 1 else -1,
        'version': current_app.config['PROJECT_VERSION'],
        'db': {
            'status': 'online',
            'time': round((time.time() - start) * 1000)
        }
    })


@frontend.route('/browserconfig.xml')
def browserconfig_xml():
    return render_template('browserconfig.xml')


@frontend.route('/die-idee')
def die_idee():
    return render_template('idee.html')


@frontend.route('/ueber-uns')
def ueber_uns():
    return render_template('ueber-uns.html')


@frontend.route('/mitmachen')
def mitmachen():
    return render_template('mitmachen.html')


@frontend.route('/api')
def api():
    return render_template('api.html')


@frontend.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')


@frontend.route('/impressum')
def impressum():
    return render_template('impressum.html')


@frontend.route('/client')
def client_test():
    return render_template('client.html')
