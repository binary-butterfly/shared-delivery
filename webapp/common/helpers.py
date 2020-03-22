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

import re
import pytz
import json
import codecs
import requests
from dateutil.parser import parse as dateutil_parse
import translitcodec
from decimal import Decimal
from datetime import datetime, timedelta
from flask.json import JSONEncoder as BaseJSONEncoder
from passlib.hash import bcrypt
from ..extensions import logger
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError
from json.decoder import JSONDecodeError


def localtime(value):
    if not value:
        return value
    if type(value) == str:
        value = dateutil_parse(value)
    if not value.tzinfo:
        value = pytz.UTC.localize(value).astimezone(pytz.timezone('Europe/Berlin'))
    return value.strftime('%Y-%m-%dT%H:%M:%S')


def send_json(url, data, log, message, auth=None):
    data = json.dumps(data, cls=DefaultJSONEncoder)
    headers = {
        'content-type': 'application/json'
    }
    try:
        kwargs = {}
        if auth:
            kwargs['auth'] = auth
        r = requests.post(url, data=data, headers=headers, **kwargs)
        return r.json()
    except (ConnectionError, NewConnectionError, JSONDecodeError):
        logger.error(log, message)
        return None


def hash_password(password, salt=False):
    if salt:
        return bcrypt.hash(password, salt=salt)
    return bcrypt.hash(password)


def get_current_time():
    return datetime.utcnow()


def get_current_time_plus(days=0, hours=0, minutes=0, seconds=0):
    return get_current_time() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, Decimal):
            return str(obj)
        return obj.__dict__


def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

    result = []
    for word in _punct_re.split(text.lower()):
        word = codecs.encode(word, 'translit/long')
        if word:
            result.append(word)
    return delim.join(result)


