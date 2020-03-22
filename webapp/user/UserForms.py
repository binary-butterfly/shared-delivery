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

from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import validators
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField


class LoginForm(FlaskForm):
    email = StringField(
        _('E-Mail'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie eine E-Mail-Adresse an')
            )
        ]
    )
    password = PasswordField(
        _('Passwort'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie ein Passwort ein.')
            )
        ]
    )
    remember_me = BooleanField(
        _('Eingeloggt bleiben'),
        default=False
    )
    submit = SubmitField(_('login'))


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        _('Altes Passwort')
    )
    new_password = PasswordField(
        _('Neues Passwort'),
        [
            validators.Length(
                min=8,
                message=_('Passwort muss aus mindestens 8 Buchstaben bestehen.')
            )
        ]
    )
    confirm = PasswordField(
        _('Neues Passwort (Wiederholung)'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie ein Passwort ein.')
            ),
            validators.EqualTo(
                'new_password',
                message=_('Passwörter müssen identisch sein.')
            )
        ]
    )
    submit = SubmitField(_('Passwort speichern'))


class UserProfileForm(FlaskForm):
    first_name = StringField(
        label=_('Vorname'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Vorname an.')
            )
        ]
    )
    last_name = StringField(
        label=_('Nachname'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Nachnamen an.')
            )
        ]
    )
    company = StringField(
        label=_('Unternehmen')
    )
    address = StringField(
        label=_('Strasse und Hausnummer'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie Strasse und Hausnummer an.')
            )
        ]
    )
    postalcode = StringField(
        label=_('Postleitzahl'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie eine Postleitzahl an.')
            )
        ]
    )
    locality = StringField(
        label=_('Ort'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Ort an.')
            )
        ]
    )
    language = SelectField(
        label=_('Sprache'),
        choices=[('de', _('deutsch')), ('en', _('englisch'))],
        default='de'
    )
    phone = StringField(
        label=_('Telefonnummer'),
        validators=[]
    )
    submit = SubmitField(_('speichern'))


class RecoverForm(FlaskForm):
    email = StringField(
        _('E-Mail Adresse'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie eine E-Mail-Adresse an')
            ),
            validators.Email(
                message=_('Bitte geben Sie eine korrekte Mailadresse an.')
            )
        ]
    )
    submit = SubmitField(_('Password via E-Mail anfordern'))


class RecoverSetForm(FlaskForm):
    password = PasswordField(
        _('Passwort'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie ein Passwort ein.')
            ),
            validators.Length(
                min=6,
                max=128,
                message=_('Passwort muss aus mindestens %s Buchstaben bestehen.') % (6)
            )
        ]
    )
    password_repeat = PasswordField(
        _('Passwort (Wiederholung)'),
        [
            validators.DataRequired(
                message=_('Bitte geben Sie ein Passwort ein.')
            ),
            validators.EqualTo('password', message=_('Passwörter müssen identisch sein.'))
        ]
    )
    remember_me = BooleanField(_('Anschließend eingeloggt bleiben'), default=False)
    submit = SubmitField(_('Passwort speichern'))


class UserSettingsForm(FlaskForm):
    email_notification = SelectField(
        label=_('E-Mail Benachrichtigung'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie eine Form der E-Mail Benachrichtigung an.')
            )
        ],
        choices=[
            ('none', 'keine'),
            ('instant', 'sofort')
        ]
    )
    submit = SubmitField(_('Einstellungen speichern'))
