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

import json
from passlib.hash import bcrypt
from passlib import pwd
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from hashlib import sha256
from flask import current_app, render_template
from flask_login import login_user, UserMixin
from ..extensions import login_manager
from flask_login import AnonymousUserMixin

from ..extensions import db, mail
from .base import BaseModel


class AnonymousUser(AnonymousUserMixin):
    id = None
    states = []

    def has_capability(self, capability):
        return False


login_manager.anonymous_user = AnonymousUser


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'user'

    fields = [
        'id', 'created', 'firstname', 'lastname', 'company', 'address', 'postalcode', 'locality', 'phone', 'mobile',
        'email'
    ]

    version = '0.9.1'

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    _email = db.Column('email', db.String(255), unique=True)
    _password = db.Column('password', db.String(255), nullable=False)

    login_datetime = db.Column(db.DateTime)
    last_login_datetime = db.Column(db.DateTime)
    login_ip = db.Column(db.String(64))
    last_login_ip = db.Column(db.String(64))
    failed_login_count = db.Column(db.Integer)
    last_failed_login_count = db.Column(db.Integer)

    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    company = db.Column(db.String(255))
    address = db.Column(db.String(255))
    postalcode = db.Column(db.String(255))
    locality = db.Column(db.String(255))
    country = db.Column(db.String(2))

    language = db.Column(db.Enum('de', 'en'), default='de')

    phone = db.Column(db.String(255))
    mobile = db.Column(db.String(255))

    _capabilities = db.Column('capabilities', db.Text)

    # force email to lower
    def _get_email(self):
        return self._email

    def _set_email(self, email):
        self._email = email.lower()

    email = db.synonym('_email', descriptor=property(_get_email, _set_email))

    # password should be encrypted
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = bcrypt.hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        """
        Ueberprueft das Passwort des Nutzers
        """
        if self.password is None:
            return False
        return bcrypt.verify(password, self.password)

    @classmethod
    def authenticate(self, email, password, remember):
        """
        Authentifiziert einen Nutzer
        """
        user = User.query.filter(User.email == email).first()

        if user:
            authenticated = user.check_password(password)
            if authenticated:
                login_user(user, remember=bool(remember))
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def email_exists(self, email, exclude_id=None):
        user = User.query.filter_by(email=email)
        if exclude_id:
            user = user.filter(User.id != exclude_id)
        return user.count() > 0

    def send_validation_email(self):
        recover_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        validation_url = "%s/validate-email?id=%s" % (
            current_app.config['PROJECT_URL'],
            recover_serializer.dumps(
                [self.id, sha256(str.encode(self.password)).hexdigest()],
                salt=current_app.config['SECURITY_PASSWORD_SALT']
            )
        )
        template = 'emails/validate-email.txt'
        msg = Message(
            "Willkommen bei Shared Delivery",
            sender=current_app.config['MAILS_FROM'],
            recipients=[self.email],
            body=render_template(template, user=self, validation_url=validation_url)
        )
        mail.send(msg)

    def send_recover_email(self):
        recover_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        validation_url = "%s/recover-check?id=%s" % (
            current_app.config['PROJECT_URL'],
            recover_serializer.dumps([self.id, sha256(str.encode(self.password)).hexdigest()],
                                     salt=current_app.config['SECURITY_PASSWORD_SALT'])
        )
        msg = Message(
            "Ihr Passwort soll geändert werden",
            sender=current_app.config['MAILS_FROM'],
            recipients=[self.email],
            body=render_template('emails/recover-email.txt', user=self, validation_url=validation_url)
        )
        mail.send(msg)

    def _get_capabilities(self):
        if not self._capabilities:
            return []
        return json.loads(self._capabilities)

    def _set_capabilities(self, capabilities):
        if capabilities:
            self._capabilities = json.dumps(capabilities)

    capabilities = db.synonym('_capabilities', descriptor=property(_get_capabilities, _set_capabilities))

    def has_capability(self, *capabilities):
        if not self.capabilities:
            return False
        if 'admin' in self.capabilities:
            return True
        for capability in capabilities:
            if capability in self.capabilities:
                return True
        return False

    def __repr__(self):
        return '<User %s>' % self.email


class AnonymousUser(AnonymousUserMixin):
    id = None
    type = 'guest'

    def has_capability(self, *capabilities):
        return False

