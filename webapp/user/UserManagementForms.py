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
from wtforms import StringField, SubmitField, SelectField
from ..common.form import SearchBaseForm


class UserSearchForm(SearchBaseForm):
    name = StringField(
        label='Name'
    )
    sort_field = SelectField(
        label='Sortier-Feld',
        choices=[
            ('lastname', 'Nachname'),
            ('created', 'Erstellt')
        ]
    )


class UserForm(FlaskForm):
    firstname = StringField(
        label=_('Vorname'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Vorname an.')
            )
        ]
    )
    lastname = StringField(
        label=_('Nachname'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Nachnamen an.')
            )
        ]
    )
    email = StringField(
        label=_('E-Mail'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie eine E-Mail an.')
            ),
            validators.Email(
                message=_('Bitte geben Sie eine E-Mail an.')
            )
        ]
    )
    company = StringField(
        label=_('Unternehmen')
    )
    address = StringField(
        label=_('Strasse und Hausnummer')
    )
    postalcode = StringField(
        label=_('Postleitzahl')
    )
    locality = StringField(
        label=_('Ort')
    )
    phone = StringField(
        label=_('Telefonnummer'),
        validators=[]
    )
    submit = SubmitField(_('speichern'))


class UserAdminForm(UserForm):
    pass