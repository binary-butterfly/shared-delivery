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
    PROJECT_VERSION = '1.0.15'

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
    OVERPASS_WAIT_TIME = 20
    OVERPASS_SOURCES = {
        "shop": {
            "alcohol": {"osm": True, "summary": 3, "name": "Spirituosenladen"},
            "bakery": {"osm": True, "summary": 3, "name": "Bäckerei, Konditorei"},
            "beverages": {"osm": True, "summary": 3, "name": "Getränkemarkt"},
            "butcher": {"osm": True, "summary": 3, "name": "Metzgerei, Fleischerei"},
            "cheese": {"osm": True, "summary": 3, "name": "Käseladen"},
            "chocolate": {"osm": True, "summary": 3, "name": "Schokoladenladen"},
            "coffee": {"osm": True, "summary": 3, "name": "Kaffeeladen"},
            "confectionery": {"osm": True, "summary": 3, "name": "Süßwarenhändler"},
            "convenience": {"osm": True, "summary": 3, "name": "Kleines Lebensmittelgeschäft"},
            "deli": {"osm": True, "summary": 3, "name": "Feinkostladen"},
            "farm": {"osm": True, "summary": 3, "name": "Hofladen"},
            "greengrocer": {"osm": True, "summary": 3, "name": "Obst- und Gemüsehändler"},
            "health_food": {"osm": True, "summary": 3, "name": "Naturkost- oder Bioladen"},
            "pastry": {"osm": True, "summary": 3, "name": "Konditoreiwaren"},
            "seafood": {"osm": True, "summary": 3, "name": "Fischfachgeschäft"},
            "spices": {"osm": True, "summary": 3, "name": "Gewürzladen"},
            "tea": {"osm": True, "summary": 3, "name": "Teegeschäft"},

            "department_store": {"osm": True, "summary": 3, "name": "Warenhaus, Kaufhaus"},
            "general": {"osm": True, "summary": 3, "name": "Gemischtwarenhandlung, Dorfladen"},
            "kiosk": {"osm": True, "summary": 3, "name": "Kiosk, Büdchen"},
            "supermarket": {"osm": True, "summary": 3, "name": "Supermarkt, Einkaufszentrum"},

            "baby_goods": {"osm": True, "summary": 3, "name": "Babyfachmarkt"},

            "chemist": {"osm": True, "summary": 3, "name": "Drogerie"},
            "hairdresser": {"osm": True, "summary": 4, "name": "Frisör"},
            "hearing_aids": {"osm": True, "summary": 4, "name": "Hörgeräteakustiker"},
            "medical_supply": {"osm": True, "summary": 3, "name": "Sanitätshaus"},
            "optician": {"osm": True, "summary": 4, "name": "Optiker"},

            "appliance": {"osm": True, "summary": 5, "name": "Haushaltsgeräte"},
            "doityourself": {"osm": True, "summary": 5, "name": "Baumarkt"},
            "electrical": {"osm": True, "summary": 5, "name": "Elektronikmarkt"},
            "florist": {"osm": True, "summary": 3, "name": "Florist, Blumenladen, Blumenhandel"},
            "garden_centre": {"osm": True, "summary": 5, "name": "Garten-Center"},
            "houseware": {"osm": True, "summary": 3, "name": "Haushaltsartikel"},
            "locksmith": {"osm": True, "summary": 3, "name": "Schlüsseldienst"},
            "trade": {"osm": True, "summary": 5, "name": "Baustoffhandel"},

            "furniture": {"osm": True, "summary": 3, "name": "Möbelhaus, Einrichtungshaus, Wohnstudio"},
            "computer": {"osm": True, "summary": 3, "name": "Computer-Fachhändler"},
            "mobile_phone": {"osm": True, "summary": 3, "name": "Handy-Shop"},

            "bicycle": {"osm": True, "summary": 5, "name": "Fahrradgeschäft"},
            "car": {"osm": True, "summary": 5, "name": "Autohaus"},
            "car_repair": {"osm": True, "summary": 5, "name": "Autowerkstatt, Reifenservice"},
            "fuel": {"osm": True, "summary": 5, "name": "Brennstoff"},
            "sports": {"osm": True, "summary": 3, "name": "Sportbedarf"},

            "craft": {"osm": True, "summary": 3, "name": "Künstler- und Bastelbedarf"},
            "musical_instrument": {"osm": True, "summary": 3, "name": "Musikinstrumentengeschäft"},

            "books": {"osm": True, "summary": 3, "name": "Buchhandlung"},
            "newsagent": {"osm": True, "summary": 3, "name": "Zeitungshändler, Lottoladen"},
            "stationery": {"osm": True, "summary": 3, "name": "Schreibwaren, Bürobedarf"},

            "dry_cleaning": {"osm": True, "summary": 4, "name": "Chemische Reinigung"},
            "funeral_directors": {"osm": True, "summary": 4, "name": "Bestattungsunternehmen"},
            "laundry": {"osm": True, "summary": 4, "name": "Reinigung, Waschsalon"},
            "pet": {"osm": True, "summary": 3, "name": "Zoo- oder Tierhandlung"},
            "toys": {"osm": True, "summary": 3, "name": "Spielzeuggeschäft"},

            "private_engagement": {"osm": False, "summary": 6, "name": "Nachbarschaftshilfe, private Angebote"},
            "club": {"osm": False, "summary": 6, "name": "Vereine helfen"}
        },
        "amenity": {
            "bar": {"osm": True, "summary": 2, "name": "Bar"},
            "cafe": {"osm": True, "summary": 2, "name": "Café, Eiscafé, Bistro, Teeladen, Kaffeeladen"},
            "fast_food": {"osm": True, "summary": 2, "name": "Schnell-Restaurant, Imbiss"},
            "ice_cream": {"osm": True, "summary": 2, "name": "Eisdiele"},
            "pub": {"osm": True, "summary": 2, "name": "Kneipe"},
            "restaurant": {"osm": True, "summary": 2, "name": "Restaurant"},

            "fuel": {"osm": True, "summary": 5, "name": "Tankstelle"},

            "clinic": {"osm": True, "summary": 1, "name": "Klinik"},
            "dentist": {"osm": True, "summary": 1, "name": "Zahnarztpraxis"},
            "doctors": {"osm": True, "summary": 1, "name": "Arztpraxis"},
            "hospital": {"osm": True, "summary": 1, "name": "Krankenhaus"},
            "pharmacy": {"osm": True, "summary": 1, "name": "Apotheke"},
            "veterinary": {"osm": True, "summary": 1, "name": "Tierarztpraxis"},

            "public_bookcase": {"osm": True, "summary": 4, "name": "Bücherschrank"},
            "animal_boarding": {"osm": True, "summary": 4, "name": "Tierpension"},
            "animal_shelter": {"osm": True, "summary": 4, "name": "Tierheim"},
            "childcare": {"osm": True, "summary": 4, "name": "Kinderbetreuung"},
            "internet_cafe": {"osm": True, "summary": 4, "name": "Internet Café"},
            "marketplace": {"osm": True, "summary": 3, "name": "Markt"},
            "place_of_worship": {"osm": True, "summary": 4, "name": "Religiöse Einrichtung"},
            "post_office": {"osm": True, "summary": 3, "name": "Postamt"}
        }
    }

    SUMMARIZE_CATEGORIES = {
        1: {
            'name': 'Ärztliche Versorgung',
            'slug': 'medical-care',
        },
        2: {
            'name': 'Gastronomie',
            'slug': 'gastronomy'
        },
        3: {
            'name': 'Einzelhandel',
            'slug': 'retail'
        },
        4: {
            'name': 'Dienstleistungen',
            'slug': 'services'
        },
        5: {
            'name': 'Gewerbe',
            'slug': 'trade'
        },
        6: {
            'name': 'Private Angebote',
            'slug': 'private-offers'
        },
        0: {
            'name': 'Weiteres',
            'slug': 'misc'
        }
    }
