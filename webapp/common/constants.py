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


class BaseConfig:
    INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

    PROJECT_NAME = "shared-delivery"
    PROJECT_VERSION = '1.0.8'

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'logs'))
    TEMP_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'temp'))
    IMG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'static', 'img'))

    DEBUG = False
    TESTING = False
    MAINTENANCE_MODE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    CELERY_RESULT_BACKEND = 'amqp://localhost'
    CELERY_BROKER_URL = 'amqp://localhost'

    ELASTICSEARCH_HOST = 'localhost'

    BABEL_DEFAULT_LOCALE = 'de'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Berlin'

    MAPBOX_CENTER_LAT = 51.470915
    MAPBOX_CENTER_LON = 7.219874
    MAPBOX_ZOOM = 13

    ITEMS_PER_PAGE = 25
    ITEMS_PER_API = 25

    THUMBNAIL_SIZES = [
        [1110, 555],
        [350, 175]
    ]

    ELASTICSEARCH_STORE_INDEX = 'shared-delivery-store'

    OVERPASS_BASE_URL = 'https://overpass-api.de/api/interpreter'

    OVERPASS_SOURCES = {
        'shop': {
            'bakery': 'Bäckerei, Konditorei',
            'beverages': 'Getränkemarkt',
            'butcher': 'Metzgerei, Fleischerei',
            'cheese': 'Käseladen',
            'chocolate': 'Schokoladenladen',
            'coffee': 'Kaffeeladen',
            'confectionery': 'Süßwarenhändler',
            'convenience': 'Dorfladen, Kiosk, Hofladen',
            'gasstation': 'Tankstelle',
            'deli': 'Feinkostladen',
            'greengrocer': 'Obst- und Gemüsehändler',
            'health_food': 'Naturkost- oder Bioladen',
            'seafood': 'Fischfachgeschäft',
            'spices': 'Gewürzladen',
            'tea': 'Teegeschäft',
            'department_store': 'Kaufhaus',
            'supermarket': 'Supermarkt, Einkaufszentrum',
            'baby_goods': 'Babyfachmarkt',
            'chemist': 'Drogerie',
            'hairdresser': 'Frisör',
            'hearing_aids': 'Hörgeräteakustiker',
            'medical_supply': 'Sanitätshaus',
            'optician': 'Optiker',
            'appliance': 'Haushaltsgeräte',
            'doityourself': 'Baumarkt',
            'electrical': 'Elektronikmarkt',
            'florist': 'Florist, Blumenladen, Blumenhandel',
            'garden_centre': 'Garten-Center',
            'locksmith': 'Schlüsseldienst',
            'trade': 'Baustoffhandel',
            'furniture': 'Möbelhaus, Einrichtungshaus, Wohnstudio',
            'computer': 'Computer-Fachhändler',
            'mobile_phone': 'Handy-Shop',
            'bicycle': 'Fahrradgeschäft, Fahrradwerkstatt, Fahrradverleih, Fahrradservice',
            'car': 'Autohaus',
            'car_repair': 'Autowerkstatt, Autoreparatur, Reifenservice',
            'fuel': 'Brennstoff',
            'sports': 'Sportbedarf',
            'craft': 'Künstler- und Bastelbedarf',
            'musical_instrument': 'Musikhaus, Musikinstrumentengeschäft',
            'books': 'Buchhandlung',
            'newsagent': 'Zeitungshändler, Lottoladen',
            'stationery': 'Schreibwaren, Bürobedarf',
            'dry_cleaning': 'Chemische Reinigung',
            'funeral_directors': 'Bestattungsunternehmen',
            'laundry': 'Wäscherei, Reinigung, Waschsalon',
            'pet': 'Zoo- oder Tierhandlung',
            'toys': 'Spielzeuggeschäft',
            'private_engagement': 'Nachbarschaftshilfe, private Angebote',
            'club': 'Vereine helfen'
        },
        'amenity': {
            'doctors': 'Arztpraxis, Ärztehaus',
            'cafe': 'Café, Eiscafé, Bistro',
            'restaurant': 'Restaurant',
            'pub': 'Kneipe',
            'fast_food': 'Schnell-Restaurant, Imbiss',
            'bar': 'Bar, Nachtlokal'
        }
    }
