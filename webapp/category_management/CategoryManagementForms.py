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

from flask import current_app
from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import validators
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from ..common.form import SearchBaseForm
from ..common.form_validator import ValidateMimeType
from ..common.form_field import ExtendedFileField, SummarizeCategoryField


class CategorySearchForm(SearchBaseForm):
    name = StringField(
        label='Name'
    )
    sort_field = SelectField(
        label='Sortier-Feld',
        choices=[
            ('name', 'Name'),
            ('created', 'Erstellt')
        ]
    )


class CategoryForm(FlaskForm):
    class Meta:
        locales = ('de_DE', 'de')

    name = StringField(
        label=_('Name'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Namen an.')
            )
        ]
    )
    description = TextAreaField(
        label='Beschreibung'
    )
    logo = ExtendedFileField(
        label='Logo',
        validators=[
            ValidateMimeType(
                mimetypes=['image/jpeg', 'image/png', 'image/svg+xml'],
                allow_empty=True,
                message='Bitte ein PNG-, JPG- oder SVG-Bild hochladen!'
            )
        ]
    )
    picture = ExtendedFileField(
        label='Bild',
        validators=[
            ValidateMimeType(
                mimetypes=['image/jpeg', 'image/png', 'image/svg+xml'],
                allow_empty=True,
                message='Bitte ein PNG-, JPG- oder SVG-Bild hochladen!'
            )
        ]
    )
    summarize_category = SummarizeCategoryField(
        label='Übergeordnete Kategorie'
    )
    submit = SubmitField(_('speichern'))


class CategoryDeleteForm(FlaskForm):
    submit = SubmitField(_('löschen'))
    abort = SubmitField(_('abbrechen'))
