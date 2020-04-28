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
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField, FormField, FieldList, \
    BooleanField
from ..common.form import SearchBaseForm
from ..common.form_field import RegionField, CategoryField, TimeStringField
from ..common.form_validator import ValidateMimeType
from ..common.form_filter import float_filter
from ..common.form_field import ExtendedFileField


class StoreSearchForm(SearchBaseForm):
    name = StringField(
        label='Name'
    )
    region = RegionField(
        label='Region',
        all_option=True,
        limit_allowed=True,
        none_entry=True,
        validators=[
            validators.Optional()
        ]
    )
    revisit_required = SelectField(
        label='Benötigt überarbeitung',
        choices=[
            ('_all', 'beliebig'),
            ('yes', 'ja'),
            ('no', 'nein')
        ],
        validators=[
            validators.Optional()
        ]
    )
    sort_field = SelectField(
        label='Sortier-Feld',
        choices=[
            ('name', 'Name'),
            ('created', 'Erstellt')
        ]
    )


class StoreSuggestionSearchForm(SearchBaseForm):
    region = RegionField(
        label='Region',
        all_option=True,
        limit_allowed=True,
        none_entry=True,
        validators=[
            validators.Optional()
        ]
    )
    settled = SelectField(
        label='erledigt',
        choices=[
            ('_all', 'beliebig'),
            ('yes', 'ja'),
            ('no', 'nein')
        ],
        validators=[
            validators.Optional()
        ],
        default='no'
    )
    sort_field = SelectField(
        label='Sortier-Feld',
        choices=[
            ('created', 'Erstellt')
        ]
    )


class OpeningTimeForm(FlaskForm):
    weekday = SelectField(
        label='Wochentag',
        choices=[
            ('1', 'Montags'),
            ('2', 'Dienstags'),
            ('3', 'Mittwoch'),
            ('4', 'Donnerstag'),
            ('5', 'Freitag'),
            ('6', 'Samstag'),
            ('7', 'Sonntag')
        ]
    )
    open = TimeStringField(
        label='Öffnungszeit'
    )
    close = TimeStringField(
        label='Schließzeit'
    )


class StoreBaseForm(FlaskForm):
    class Meta:
        locales = ('de_DE', 'de')

    name = StringField(
        label=_('Name'),
        validators=[
            validators.DataRequired(
                message=_('Bitte geben Sie einen Namen an.')
            ),
            validators.Length(
                max=256,
                message='Der Name darf maximal 256 Zeichen lang sein.'
            )
        ]
    )
    category = CategoryField(
        label=_('Art des Geschäfts'),
        validators=[
            validators.DataRequired(
                message='Bitte geben Sie mindestens eine Kategorie an.'
            )
        ]
    )
    source_text = StringField(
        label=_('Woher kommt die Information?')
    )
    source_url = StringField(
        label=_('Woher kommt die Information (Ergänzender Link)?'),
        validators=[
            validators.URL(
                message='Bitte geben Sie eine valide URL ein (oder gar nichts)'
            ),
            validators.Optional()
        ]
    )
    company = StringField(
        label=_('Unternehmen'),
        validators=[
            validators.Length(
                max=256,
                message='Der Unternehmens-Name darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ]
    )
    address = StringField(
        label=_('Straße und Hausnummer'),
        validators=[
            validators.Length(
                max=256,
                message='Straße und Hausnummer dürfen maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ]
    )
    postalcode = StringField(
        label=_('Postleitzahl'),
        validators=[
            validators.Regexp(
                '^[0-9]{5,5}$',
                message='Die Postleitzahl muss aus fünf Zahlen bestehen'
            ),
            validators.Optional()
        ]
    )
    locality = StringField(
        label=_('Ort'),
        validators=[
            validators.Length(
                max=256,
                message='Der Ort darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ]
    )
    website = StringField(
        label=_('Website'),
        validators=[
            validators.url(
                message='Bitte geben Sie eine URL an'
            ),
            validators.Length(
                max=256,
                message='Die Website darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ],
    )
    website_coupon = StringField(
        label=_('Link zum Gutschein-Kauf'),
        validators=[
            validators.url(
                message='Bitte geben Sie eine URL an'
            ),
            validators.Length(
                max=256,
                message='Die Website darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ],
    )
    website_crowdfunding = StringField(
        label=_('Link zu einem Crowdfunding'),
        validators=[
            validators.url(
                message='Bitte geben Sie eine URL an'
            ),
            validators.Length(
                max=256,
                message='Die Website darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ],
    )
    email = StringField(
        label=_('E-Mail'),
        validators=[
            validators.email(
                message='Bitte geben Sie eine E-Mail an'
            ),
            validators.Length(
                max=256,
                message='Die E-Mail darf maximal 256 Zeichen lang sein.'
            ),
            validators.Optional()
        ],
    )
    phone = StringField(
        label=_('Telefon'),
        validators=[
            validators.Regexp(
                '^[0-9- +]{0,32}$',
                message='Die Telefonnummer darf aus maximal 32 Zahlen bestehen'
            ),
            validators.Optional()
        ]
    )
    mobile = StringField(
        label=_('Mobiltelefon'),
        validators=[
            validators.Regexp(
                '^[0-9- +]{0,32}$',
                message='Die Mobilfunknummer darf aus maximal 32 Zahlen bestehen'
            ),
            validators.Optional()
        ]
    )
    fax = StringField(
        label=_('Fax'),
        validators=[
            validators.Regexp(
                '^[0-9- +]{0,32}$',
                message='Die Faxnummer darf aus maximal 32 Zahlen bestehen'
            ),
            validators.Optional()
        ]
    )
    description = TextAreaField(
        label='Beschreibung'
    )
    all_switch = BooleanField(
        label='Geschäft hat geöffnet'
    )
    opening_times_all = FieldList(
        FormField(OpeningTimeForm),
        label='Öffnungszeiten',
        min_entries=0
    )
    delivery = BooleanField(
        label='Lieferung'
    )
    pickup = BooleanField(
        label='Abholung'
    )
    onlineshop = BooleanField(
        label='Onlineshop'
    )
    delivery_switch = BooleanField(
        label='Abweichende Lieferzeiten'
    )
    opening_times_delivery = FieldList(
        FormField(OpeningTimeForm),
        label='Öffnungszeiten',
        min_entries=0
    )
    pickup_switch = BooleanField(
        label='Abweichende Abholzeiten'
    )
    opening_times_pickup = FieldList(
        FormField(OpeningTimeForm),
        label='Öffnungszeiten',
        min_entries=0
    )
    logo = ExtendedFileField(
        label='Logo',
        validators=[
            ValidateMimeType(
                mimetypes=['image/jpeg', 'image/png', 'image/svg+xml', 'image/gif'],
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
    submit = SubmitField(_('speichern'))


class StoreForm(StoreBaseForm):
    region = RegionField(
        label=_('Region'),
        limit_allowed=True,
        validators=[
            validators.NoneOf(
                ['0'],
                message='Bitte geben Sie eine Region an'
            )
        ]
    )


class StoreNewForm(StoreForm):
    lat = HiddenField(
        label=_('Längengrad'),
        filters=[
            float_filter
        ]
    )
    lon = HiddenField(
        label=_('Breitengrad'),
        filters=[
            float_filter
        ]
    )


class StoreDeleteForm(FlaskForm):
    submit = SubmitField(_('löschen'))
    abort = SubmitField(_('abbrechen'))


class StoreSuggestionMergeForm(FlaskForm):
    merge = SubmitField(_('übernehmen'))
    delete = SubmitField(_('löschen'))
    edit = SubmitField(_('einzeln bearbeiten'))
    abort = SubmitField(_('abbrechen'))

