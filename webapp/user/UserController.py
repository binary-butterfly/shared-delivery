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

import datetime
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer
from flask import Blueprint, render_template, current_app, request, flash, redirect, session, abort
from flask_login import login_required, login_user, current_user, logout_user
from .UserForms import LoginForm, PasswordForm, RecoverForm, RecoverSetForm, UserSettingsForm
from ..models import User
from ..extensions import db, logger
from flask_babel import _


user = Blueprint('user', __name__, template_folder='templates')

from . import UserManagementController


@user.route('/login', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.email.data, form.password.data, form.remember_me.data)
        if authenticated:
            user.last_failed_login_count = user.failed_login_count
            user.failed_login_count = 0
            user.last_login_datetime = user.login_datetime
            user.login_datetime = datetime.datetime.utcnow()
            user.last_login_ip = user.login_ip
            user.login_ip = request.headers.get('X-Forwarded-For', None)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        elif user:
            flash(_('Zugangsdaten nicht korrekt'), 'danger')
            if user.failed_login_count:
                user.failed_login_count += 1
            else:
                user.failed_login_count = 1
            db.session.add(user)
            db.session.commit()
        else:
            flash(_('Zugangsdaten nicht korrekt'), 'danger')
    return render_template('login.html', form=form)


@user.route('/user/password', methods=['GET', 'POST'])
@login_required
def account_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            logger.info('user', '%s updated his / her password' % (current_user.id))
            flash(_('Neues Passwort gespeichert'), 'success')
            return redirect('/')
        else:
            flash(_('Altes Passwort nicht korrekt'), 'danger')
    return render_template('password.html', form=form)


@user.route('/logout')
def logout():
    session.pop('login', None)
    logout_user()
    flash(_('Sie haben sich erfolgreich ausgeloggt.'), 'success')
    return redirect('/')


@user.route('/recover', methods=['GET', 'POST'])
def recover():
    if current_app.config['MAINTENANCE_MODE']:
        return render_template('maintenance.html')
    form = RecoverForm()
    if form.validate_on_submit():
        recover_user = User.query.filter_by(email=form.email.data.lower())
        if recover_user.count() == 0:
            flash('Diesen Account gibt es nicht.', 'danger')
        else:
            recover_user = recover_user.first()
            recover_user.send_recover_email()
            logger.info('user', '%s sent an recovery request' % (recover_user.id))
            return render_template('recover-mail-sent.html')
    return render_template('recover.html', form=form)


@user.route('/recover-check', methods=['GET', 'POST'])
def recover_check():
    serialized_data = request.args.get('id', '')
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(
            serialized_data,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=30 * 60 * 60 * 24 * 14
        )
    except:
        return render_template('recover-fail.html')
    if not len(data) == 2:
        return render_template('recover-fail.html')

    user = User.query.filter_by(id=data[0])
    if user.count() != 1:
        return render_template('recover-fail.html')
    user = user.first()
    if sha256(str.encode(user.password)).hexdigest() != data[1]:
        return render_template('recover-fail.html')
    form = RecoverSetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        user.active = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        logger.info('user', '%s got access to his / her account after registration / recovery' % (current_user.id))
        flash('Passwort erfolgreich aktualisiert.', 'success')
        return redirect('/')
    return render_template('recover-password-set.html', form=form, url_id=serialized_data)


@user.route('/user/<int:user_id>/switch')
def user_switch(user_id):
    newuser = User.query.get(user_id)
    if not newuser:
        abort(403)
    if current_user.has_capability('admin'):
        session['emulate-user-id'] = user_id
        return redirect('/')
    abort(403)


@user.route('/user/switch-back')
def user_switch_back():
    session.pop('emulate-user-id', None)
    return redirect('/')


@user.route('/user/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    form = UserSettingsForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()

        flash(_('Einstellungen gespeichert.'), 'success')
        return redirect('/')
    return render_template('settings.html', form=form)
