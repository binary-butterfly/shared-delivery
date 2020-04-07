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
    PROJECT_VERSION = '1.0.19'

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
        "tourism": {
            "hotel": {"osm": True, "summary": 2, "name": "Hotel"}
        },
        "shop": {
            # Food, beverages
            "alcohol": {"osm": True, "summary": 3, "name": "Spirituosenladen"},
            "bakery": {"osm": True, "summary": 3, "name": "Bäckerei, Konditorei"},
            "beverages": {"osm": True, "summary": 3, "name": "Getränkemarkt"},
            "brewing_supplies": {"osm": True, "summary": 3, "name": "Brauzubehör"},
            "butcher": {"osm": True, "summary": 3, "name": "Metzgerei, Fleischerei"},
            "cheese": {"osm": True, "summary": 3, "name": "Käseladen"},
            "chocolate": {"osm": True, "summary": 3, "name": "Schokoladenladen"},
            "coffee": {"osm": True, "summary": 3, "name": "Kaffeeladen"},
            "confectionery": {"osm": True, "summary": 3, "name": "Süßwarenhändler"},
            "convenience": {"osm": True, "summary": 3, "name": "Kleines Lebensmittelgeschäft"},
            "deli": {"osm": True, "summary": 3, "name": "Feinkostladen"},
            "dairy": {"osm": True, "summary": 3, "name": "Milchprodukte"},
            "farm": {"osm": True, "summary": 3, "name": "Hofladen"},
            "frozen_food": {"osm": True, "summary": 3, "name": "Tiefkühlkost"},
            "greengrocer": {"osm": True, "summary": 3, "name": "Obst- und Gemüsehändler"},
            "health_food": {"osm": True, "summary": 3, "name": "Naturkost- oder Bioladen"},
            "ice_cream": {"osm": True, "summary": 3, "name": "Verpackte Eisprodukte"},
            "pasta": {"osm": True, "summary": 3, "name": "Frische Nudeln, Teigwaren"},
            "pastry": {"osm": True, "summary": 3, "name": "Konditoreiwaren"},
            "seafood": {"osm": True, "summary": 3, "name": "Fischfachgeschäft"},
            "spices": {"osm": True, "summary": 3, "name": "Gewürzladen"},
            "tea": {"osm": True, "summary": 3, "name": "Teegeschäft"},
            "wasser": {"osm": True, "summary": 3, "name": "Trinkwasser"},

            # General store, department store, mall
            "department_store": {"osm": True, "summary": 3, "name": "Warenhaus, Kaufhaus"},
            "general": {"osm": True, "summary": 3, "name": "Gemischtwarenhandlung, Dorfladen"},
            "kiosk": {"osm": True, "summary": 3, "name": "Kiosk, Büdchen"},
            "mall": {"osm": True, "summary": 3, "name": "Einkaufszentrum"},
            "supermarket": {"osm": True, "summary": 3, "name": "Supermarkt, Einkaufszentrum"},
            "wholesale": {"osm": True, "summary": 5, "name": "Großhandel"},

            # Clothing, shoes, accessories
            "baby_goods": {"osm": True, "summary": 3, "name": "Babyfachmarkt"},
            "bag": {"osm": True, "summary": 3, "name": "Taschen und Koffer"},
            "boutique": {"osm": True, "summary": 3, "name": "Boutique, Modehaus"},
            "clothes": {"osm": True, "summary": 3, "name": "Bekleidungsgeschäft"},
            "fabric": {"osm": True, "summary": 3, "name": "Stoffgeschäft, Textilgeschäft"},
            "fashion_accessories": {"osm": True, "summary": 3, "name": "Geschäft für Modeaccessoires"},
            "jewelry": {"osm": True, "summary": 3, "name": "Schmuck, Juwelier"},
            "leather": {"osm": True, "summary": 3, "name": "Lederwarengeschäft"},
            "sewing": {"osm": True, "summary": 3, "name": "Nähzubehör"},
            "shoes": {"osm": True, "summary": 3, "name": "Schuhgeschäft"},
            "tailor": {"osm": True, "summary": 3, "name": "Schneiderei"},
            "watches": {"osm": True, "summary": 3, "name": "Uhrengeschäft"},
            "wool": {"osm": True, "summary": 3, "name": "Wollgeschäft"},

            # Discount store, charity
            "charity": {"osm": True, "summary": 3, "name": "Gebrauchtwarenladen"},
            "second_hand": {"osm": True, "summary": 3, "name": "Second-Hand-Laden / An- und Verkauf"},
            "variety_store": {"osm": True, "summary": 3, "name": "Niedrigpreisgeschäft, Ein-Euro-Laden, Restpostenladen, Ramschladen, Kramladen"},

            # Health and beauty
            "beauty": {"osm": True, "summary": 4, "name": "Schönheits-, Kosmetiksalon, Nagelstudio, Parfümerie, Wellness-Center"},
            "chemist": {"osm": True, "summary": 3, "name": "Drogerie"},
            "cosmetics": {"osm": True, "summary": 3, "name": "Kosmetikgeschäft"},
            "erotic": {"osm": True, "summary": 3, "name": "Erotikhandel"},
            "hairdresser": {"osm": True, "summary": 4, "name": "Frisör"},
            "hairdresser_supply": {"osm": True, "summary": 5, "name": "Friseurbedarf"},
            "hearing_aids": {"osm": True, "summary": 4, "name": "Hörgeräteakustiker"},
            "herbalist": {"osm": True, "summary": 3, "name": "Kräuterhandel"},
            "massage": {"osm": True, "summary": 4, "name": "Massagesalon"},
            "medical_supply": {"osm": True, "summary": 3, "name": "Sanitätshaus"},
            "nutrition_supplements": {"osm": True, "summary": 3, "name": "Nahrungsergänzungsmittel"},
            "optician": {"osm": True, "summary": 4, "name": "Optiker"},
            "perfumery": {"osm": True, "summary": 3, "name": "Parfümerie"},
            "tattoo": {"osm": True, "summary": 4, "name": "Tattoo-Studio"},

            # Do-it-yourself, household, building materials, gardening
            "agrarian": {"osm": True, "summary": 5, "name": "Komponenten für die landwirtschaftliche Produktion"},
            "appliance": {"osm": True, "summary": 5, "name": "Haushaltsgeräte"},
            "bathrom_furnishing": {"osm": True, "summary": 3, "name": "Badezimmereinrichtung"},
            "doityourself": {"osm": True, "summary": 5, "name": "Baumarkt"},
            "electrical": {"osm": True, "summary": 5, "name": "Elektronikmarkt"},
            # "energy": {"osm": True, "summary": 5, "name": "Verkauf von Energie"},
            "fireplace": {"osm": True, "summary": 5, "name": "Kaminofen, Kachelofen"},
            "florist": {"osm": True, "summary": 3, "name": "Florist, Blumenladen, Blumenhandel"},
            "garden_centre": {"osm": True, "summary": 5, "name": "Garten-Center"},
            "garden_furniture": {"osm": True, "summary": 5, "name": "Gartenmöbel"},
            "gas": {"osm": True, "summary": 5, "name": "Gasflaschen"},
            "glaziery": {"osm": True, "summary": 5, "name": "Glaserei"},
            "hardware": {"osm": True, "summary": 5, "name": "Eisenwaren"},
            "houseware": {"osm": True, "summary": 3, "name": "Haushaltsartikel"},
            "locksmith": {"osm": True, "summary": 3, "name": "Schlüsseldienst"},
            "paint": {"osm": True, "summary": 3, "name": "Farbengeschäft"},
            "security": {"osm": True, "summary": 5, "name": "Sicherheitsausrüstung"},
            "trade": {"osm": True, "summary": 5, "name": "Baustoffhandel"},

            # Furniture and interior
            "antiques": {"osm": True, "summary": 3, "name": "Antiquitäten"},
            "bed": {"osm": True, "summary": 3, "name": "Bettengeschäft, Matratzengeschäft"},
            "candles": {"osm": True, "summary": 3, "name": "Kerzen und Zubehör"},
            "carpet": {"osm": True, "summary": 3, "name": "Teppichgeschäft"},
            "curtain": {"osm": True, "summary": 3, "name": "Gardinenfachgeschäft"},
            "doors": {"osm": True, "summary": 3, "name": "Türenfachgeschäft"},
            "flooring": {"osm": True, "summary": 3, "name": "Fußbodengeschäft"},
            "furniture": {"osm": True, "summary": 3, "name": "Möbelhaus, Einrichtungshaus, Wohnstudio"},
            "interior_decoration": {"osm": True, "summary": 3, "name": "Innendekoration, Raumausstattung"},
            "kitchen": {"osm": True, "summary": 3, "name": "Küchengeschäft"},
            "lighting": {"osm": True, "summary": 3, "name": "Lampengeschäft"},
            "tiles": {"osm": True, "summary": 3, "name": "Fliesenhändler"},
            "window_blind": {"osm": True, "summary": 3, "name": "Jalousien- oder Rollladenverkauf"},

            # Electronics
            "computer": {"osm": True, "summary": 3, "name": "Computer-Fachhändler"},
            "robot": {"osm": True, "summary": 3, "name": "Roboter"},
            "electronics": {"osm": True, "summary": 3, "name": "Elektronikmarkt"},
            "hifi": {"osm": True, "summary": 3, "name": "Hifi-Fachhändler"},
            "mobile_phone": {"osm": True, "summary": 3, "name": "Handy-Shop"},
            "radiotechnics": {"osm": True, "summary": 3, "name": "Elektronische Bauteile"},
            "vacuum_cleaner": {"osm": True, "summary": 3, "name": "Staubsaugerfachgeschäft"},

            # Outdoors and sport, vehicles
            "atv": {"osm": True, "summary": 5, "name": "ATV / Quads"},
            "bicycle": {"osm": True, "summary": 5, "name": "Fahrradgeschäft"},
            "boat": {"osm": True, "summary": 5, "name": "Boote und -zubehör"},
            "car": {"osm": True, "summary": 5, "name": "Autohaus"},
            "car_repair": {"osm": True, "summary": 5, "name": "Autowerkstatt, Reifenservice"},
            "car_parts": {"osm": True, "summary": 5, "name": "Autoteilefachgeschäft"},
            "caravan": {"osm": True, "summary": 5, "name": "Wohnwagen, Wohnmobile"},
            "fuel": {"osm": True, "summary": 5, "name": "Brennstoffe"},
            "fishing": {"osm": True, "summary": 3, "name": "Angelladen"},
            # "free_flying": {"osm": True, "summary": 5, "name": "Freiflugzubehör"},
            "golf": {"osm": True, "summary": 3, "name": "Golfsport"},
            "hunting": {"osm": True, "summary": 3, "name": "Jagdausrüstung"},
            "jetski": {"osm": True, "summary": 5, "name": "Jet-Skis, Wassermotorräder"},
            "military_surplus": {"osm": True, "summary": 3, "name": "Militärausrüstung"},
            "motorcycle": {"osm": True, "summary": 5, "name": "Motorradgeschäft"},
            "outdoor": {"osm": True, "summary": 3, "name": "Ausrüstungsladen für Freiluftaktivitäten"},
            "scuba_diving": {"osm": True, "summary": 3, "name": "Tauchausrüstungsladen"},
            "ski": {"osm": True, "summary": 3, "name": "Skis und Skiausrüstung"},
            "snowmobile": {"osm": True, "summary": 5, "name": "Schneemobile, Motorschlitten"},
            "sports": {"osm": True, "summary": 3, "name": "Sportbedarf"},
            "swimming_pool": {"osm": True, "summary": 5, "name": "Schwimmbäder, Pools, Schwimmbadzubehör"},
            "trailer": {"osm": True, "summary": 5, "name": "Anhängerzubehör"},
            "tyres": {"osm": True, "summary": 4, "name": "Reifenservice"},

            # Art, music, hobbies
            "art": {"osm": True, "summary": 3, "name": "Kunstladen"},
            "collector": {"osm": True, "summary": 3, "name": "Sammlerartikel, Briefmakren, Münzen, Action Figuren"},
            "craft": {"osm": True, "summary": 3, "name": "Künstler- und Bastelbedarf"},
            "frame": {"osm": True, "summary": 3, "name": "Bilderrahmengeschäft"},
            "games": {"osm": True, "summary": 3, "name": "Brettspiele, Kartenspiele, Rollenspiele"},
            "model": {"osm": True, "summary": 3, "name": "Modellbau"},
            "music": {"osm": True, "summary": 3, "name": "Musikgeschäft"},
            "musical_instrument": {"osm": True, "summary": 3, "name": "Musikhaus, Musikinstrumentengeschäft"},
            "photo": {"osm": True, "summary": 3, "name": "Fotoladen"},
            "camera": {"osm": True, "summary": 3, "name": "Fotofachgeschäft"},
            "trophy": {"osm": True, "summary": 3, "name": "Pokalgeschäft"},
            "video": {"osm": True, "summary": 4, "name": "Videothek"},
            "video_games": {"osm": True, "summary": 4, "name": "Fachgeschäft für Videospiele"},

            # Stationery, gifts, books, newspapers
            "anime": {"osm": True, "summary": 3, "name": "Anime-Artikel"},
            "books": {"osm": True, "summary": 3, "name": "Buchhandlung"},
            "gift": {"osm": True, "summary": 3, "name": "Andenkenladen, Grußkarten, kleine Geschenke"},
            "lottery": {"osm": True, "summary": 4, "name": "Lottoladen"},
            "newsagent": {"osm": True, "summary": 3, "name": "Zeitungshändler"},
            "stationery": {"osm": True, "summary": 3, "name": "Schreibwaren, Bürobedarf"},
            "ticket": {"osm": True, "summary": 3, "name": "Ticketshop, Eintrittskarten, Fahrkarten"},

            # Others
            "bookmarker": {"osm": True, "summary": 4, "name": "Wettbüro"},
            "cannabis": {"osm": True, "summary": 3, "name": "Cannabis Produkte"},
            "copyshop": {"osm": True, "summary": 4, "name": "Kopierladen, Copyshop"},
            "dry_cleaning": {"osm": True, "summary": 4, "name": "Chemische Reinigung"},
            "e-cigarette": {"osm": True, "summary": 3, "name": "Elektronische Zigaretten"},
            "funeral_directors": {"osm": True, "summary": 4, "name": "Bestattungsunternehmen"},
            "laundry": {"osm": True, "summary": 4, "name": "Reinigung, Waschsalon"},
            "money_lender": {"osm": True, "summary": 4, "name": "Geldverleiher"},
            "party": {"osm": True, "summary": 3, "name": "Partyzubehör"},
            "pawnbroker": {"osm": True, "summary": 4, "name": "Pfandleiher"},
            "pet": {"osm": True, "summary": 3, "name": "Zoohandlung, Tierhandlung"},
            "pet_grooming": {"osm": True, "summary": 3, "name": "Tiersalon"},
            "pest_control": {"osm": True, "summary": 4, "name": "Schädlingsbekämpfung"},
            "pyrotechnics": {"osm": True, "summary": 3, "name": "Feuerwerkfachgeschäft"},
            "religion": {"osm": True, "summary": 3, "name": "Kloster- oder Kirchenladen"},
            "storage_rental": {"osm": True, "summary": 5, "name": "Mietlager"},
            "tobacco": {"osm": True, "summary": 3, "name": "Tabakwaren"},
            "toys": {"osm": True, "summary": 3, "name": "Spielzeuggeschäft"},
            "travel_agency": {"osm": True, "summary": 4, "name": "Reisebüro"},
            # "vacant": {"osm": True, "summary": 0, "name": "Leerstehendes Ladenlokal"},
            "weapons": {"osm": True, "summary": 3, "name": "Waffenladen"},
            "outpost": {"osm": True, "summary": 4, "name": "Abholstation"},

            # Custom tags
            "private_engagement": {"osm": False, "summary": 6, "name": "Nachbarschaftshilfe, private Angebote"},
            "club": {"osm": False, "summary": 6, "name": "Vereine helfen"}
        },
        "amenity": {
            # Sustenance
            "bar": {"osm": True, "summary": 2, "name": "Bar"},
            "bbq": {"osm": True, "summary": 0, "name": "Grillplatz"},
            "biergarten": {"osm": True, "summary": 2, "name": "Biergarten"},
            "cafe": {"osm": True, "summary": 2, "name": "Café, Eiscafé, Bistro, Teeladen, Kaffeeladen"},
            #"drinking_water": {"osm": True, "summary": 0, "name": "Trinkwasserstelle"},
            "fast_food": {"osm": True, "summary": 2, "name": "Schnell-Restaurant, Imbiss"},
            "food_court": {"osm": True, "summary": 2, "name": "Food Court, Verkaufsstellen verschiedener Restaurants und Imbisse"},
            "ice_cream": {"osm": True, "summary": 2, "name": "Eisdiele"},
            "pub": {"osm": True, "summary": 2, "name": "Kneipe"},
            "restaurant": {"osm": True, "summary": 2, "name": "Restaurant"},

            # Education
            "college": {"osm": True, "summary": 7, "name": "Hochschule"},
            "driving_school": {"osm": True, "summary": 4, "name": "Fahrschule"},

            "kindergarten": {"osm": True, "summary": 7, "name": "Kindergarten"},
            "language_school": {"osm": True, "summary": 7, "name": "Sprachschule"},
            "library": {"osm": True, "summary": 4, "name": "Bibliothek, Bücherei"},
            "toy_library": {"osm": False, "summary": 4, "name": "Spiele- und Spielzeugverleih"},
            "music_school": {"osm": True, "summary": 7, "name": "Musikschule"},
            "school": {"osm": True, "summary": 7, "name": "Schule"},
            "university": {"osm": True, "summary": 7, "name": "Universität"},

            # Transportation

            #"bicycle_parking": {"osm": True, "summary": 8, "name": "Fahrradparkplatz"},
            #"bicycle_repair_station": {"osm": True, "summary": 8, "name": "Fahrrad-Reparaturbereich"},
            "bicycle_rental": {"osm": True, "summary": 4, "name": "Fahrradverleihstation"},
            "boat_rental": {"osm": True, "summary": 4, "name": "Bootsverleih"},
            #"boat_sharing": {"osm": True, "summary": 8, "name": "Bootssharing"},
            #"bus_station": {"osm": True, "summary": 8, "name": "Busbahnhof"},
            "car_rental": {"osm": True, "summary": 4, "name": "Autoverleih"},
            #"car_sharing": {"osm": True, "summary": 8, "name": "Carsharing-Station"},
            "car_wash": {"osm": True, "summary": 5, "name": "Autowaschanlage"},
            "vehicle_inspection": {"osm": True, "summary": 5, "name": "Fahrzeuginspektion"},
            #"charging_station": {"osm": True, "summary": 8, "name": "Ladestation"},
            #"ferry_terminal": {"osm": True, "summary": 8, "name": "Fährterminal"},
            "fuel": {"osm": True, "summary": 5, "name": "Tankstelle"},
            # "grit_bin": {"osm": True, "summary": 0, "name": "Streugutcontainer"},
            #"motorcycle_parking": {"osm": True, "summary": 8, "name": "Motorradparkplatz"},
            #"parking": {"osm": True, "summary": 8, "name": "Parkplatz"},
            # "parking_entrance": {"osm": True, "summary": 8, "name": "Ein- und Ausfahrten in Tiefgaragen und Parkhäuser"},
            #"parking_space": {"osm": True, "summary": 8, "name": "Parkplatzstellflächen"},
            "taxi": {"osm": True, "summary": 8, "name": "Taxistand"},

            # Financial
            "atm": {"osm": True, "summary": 9, "name": "Geldautomat / Bankomat"},
            "bank": {"osm": True, "summary": 9, "name": "Bank, Geldinstitut"},
            "bureau_de_change": {"osm": True, "summary": 9, "name": "Geldwechselbüro"},

            # Healthcare
            #"baby_hatch": {"osm": True, "summary": 1, "name": "Babyklappe"},
            "clinic": {"osm": True, "summary": 1, "name": "Klinik"},
            "dentist": {"osm": True, "summary": 1, "name": "Zahnarztpraxis"},
            "doctors": {"osm": True, "summary": 1, "name": "Arztpraxis"},
            "hospital": {"osm": True, "summary": 1, "name": "Krankenhaus"},
            "nursing_home": {"osm": True, "summary": 1, "name": "Pflegeheim"},
            "pharmacy": {"osm": True, "summary": 1, "name": "Apotheke"},
            "social_facility": {"osm": True, "summary": 1, "name": "Soziale Einrichtung, Alters-, Obdachlosen-, Kinderheim, Die Tafel etc."},
            "veterinary": {"osm": True, "summary": 1, "name": "Tierarztpraxis, Tierklinik"},

            # Entertainment, Arts & Culture
            "arts_centre": {"osm": True, "summary": 10, "name": "Kulturzentrum"},
            "brothel": {"osm": True, "summary": 10, "name": "Bordell, Freudenhaus"},
            "casino": {"osm": True, "summary": 10, "name": "Spielbank, Spielcasino"},
            "cinema": {"osm": True, "summary": 10, "name": "Kino"},
            "community_centre": {"osm": True, "summary": 10, "name": "Gemeinschaftszentrum"},
            # "fountain": {"osm": True, "summary": 10, "name": "Springbrunnen"},
            "gambling": {"osm": True, "summary": 10, "name": "Spielhalle"},
            "nightclub": {"osm": True, "summary": 10, "name": "Nachtclub, Disco"},
            "planetarium": {"osm": True, "summary": 10, "name": "Planetarium"},
            "public_bookcase": {"osm": True, "summary": 10, "name": "Bücherschrank"},
            "social_centre": {"osm": True, "summary": 10, "name": "Autonomes/soziales Zentrum"},
            "stripclub": {"osm": True, "summary": 10, "name": "Stripclub"},
            "studio": {"osm": True, "summary": 10, "name": "TV, Radio oder Musik Studio"},
            "swingerclub": {"osm": True, "summary": 10, "name": "Swingerclub"},
            "theatre": {"osm": True, "summary": 10, "name": "Theater, Oper, Schauspielhaus"},

            # Others
            

            #"baking_oven": {"osm": True, "summary": 0, "name": "Backofen"},
            # "bench": {"osm": True, "summary": 0, "name": "Parkbank"},
            "childcare": {"osm": True, "summary": 0, "name": "Kinderbetreuung"},
            # "clock": {"osm": True, "summary": 0, "name": "Uhr"},
            "conference_centre": {"osm": True, "summary": 0, "name": "Konferenzzentrum"},
            "courthouse": {"osm": True, "summary": 0, "name": "Gericht"},
            "crematorium": {"osm": True, "summary": 0, "name": "Krematorium"},
            #"dive_centre": {"osm": True, "summary": 0, "name": "Tauchbasis"},
            #"embassy": {"osm": True, "summary": 0, "name": "Botschaft, Botschaftsgebäude"},
            "fire_station": {"osm": True, "summary": 0, "name": "Feuerwache"},
            # "grave_yard": {"osm": True, "summary": 0, "name": "Gräberfeld"},
            # "hunting_stand": {"osm": True, "summary": 0, "name": "Hochsitz"},
            "internet_cafe": {"osm": True, "summary": 0, "name": "Internet Café"},
            #"kitchen": {"osm": True, "summary": 0, "name": "Öffentlich zugängliche Küche"},
            #"kneipp_water_cure": {"osm": True, "summary": 0, "name": "Fußbad im Außenbereich"},
            "marketplace": {"osm": True, "summary": 0, "name": "Markt, Wochenmarkt"},
            #"monastery": {"osm": True, "summary": 0, "name": "Kloster"},
            #"photo_booth": {"osm": True, "summary": 0, "name": "Fotoautomat"},
            "place_of_worship": {"osm": True, "summary": 0, "name": "Religiöse Einrichtung"},
            "police": {"osm": True, "summary": 0, "name": "Polizeistation"},
            #"post_box": {"osm": True, "summary": 0, "name": "Briefkasten"},
            #"post_depot": {"osm": True, "summary": 0, "name": "Postlager"},
            "post_office": {"osm": True, "summary": 0, "name": "Postamt"},
            #"prison": {"osm": True, "summary": 0, "name": "Gefängnis"},
            "public_bath": {"osm": True, "summary": 0, "name": "Badehaus, Thermalbad, Solebad"},
            "ranger_station": {"osm": True, "summary": 0, "name": "Besucherstation"},
            "recycling": {"osm": True, "summary": 0, "name": "Recycling-Einrichtung"},
            #"sanitary_dump_station": {"osm": True, "summary": 0, "name": "Sanitäre Entsorgungsstationen"},
            #"shelter": {"osm": True, "summary": 0, "name": "Unterstand"},
            #"shower": {"osm": True, "summary": 0, "name": "Duschen oder Bad"},
            #"telephone": {"osm": True, "summary": 0, "name": "Telefon"},
            #"toilets": {"osm": True, "summary": 0, "name": "Öffentliche Toilette"},
            "townhall": {"osm": True, "summary": 0, "name": "Rathaus/Gemeindeamt"},
            #"vending_machine": {"osm": True, "summary": 0, "name": "Verkaufsautomat"},
            # "waste_basket": {"osm": True, "summary": 0, "name": "Mülleimer"},
            "waste_disposal": {"osm": True, "summary": 0, "name": "Müllabgabestelle"},
            #"waste_tranfer_station": {"osm": True, "summary": 0, "name": "Müllumladestation"},
            #"watering_place": {"osm": True, "summary": 0, "name": "Wasserstelle"},

            #"water_point": {"osm": True, "summary": 0, "name": "Trinkwasserzapfstelle"},

            "animal_boarding": {"osm": True, "summary": 0, "name": "Tierpension"},
            "animal_shelter": {"osm": True, "summary": 0, "name": "Tierheim"},
        },
        'office': {
            'insurance': {"osm": True, "summary": 4, "name": "Versicherung"},
        },
        'healthcare': {
            "physiotherapist": {"osm": True, "summary": 1, "name": "Pysiotherapie"},
            "speech_therapist": {"osm": True, "summary": 1, "name": "Logopädie"},
        },
        'craft': {
            "scaffolding": {"osm": True, "summary": 5, "name": "Gerüstbau"},
            "gardener": {"osm": True, "summary": 5, "name": "Garten- und Landschaftsbau"},
            "cleaner": {"osm": True, "summary": 5, "name": "Gebäudereinigung"},
            "locksmith": {"osm": True, "summary": 5, "name": "Schlüsseldienst"},
            "carpenter": {"osm": True, "summary": 5, "name": "Schreinerei, Tischlerei"},
            "agricultural_engines": {"osm": True, "summary": 5, "name": "Landmaschinenbau, -reparatur"},
            "electrician": {"osm": True, "summary": 5, "name": "Elektriker, Elektroinstallation"},
            "painter": {"osm": True, "summary": 5, "name": "Maler"},
            "roofer": {"osm": True, "summary": 5, "name": "Dachdecker"},
            "sweep": {"osm": True, "summary": 5, "name": "Schornsteinfeger"},
            "plumber": {"osm": True, "summary": 5, "name": "Installateur, Klemptner"},
            "tiller": {"osm": True, "summary": 5, "name": "Fliesenleger"},
            "tailer": {"osm": True, "summary": 5, "name": "Schneiderei"},
            "metal_construction": {"osm": True, "summary": 5, "name": "Metallbauer"}
        }
    }

    SUMMARIZE_CATEGORIES = {
        1: {
            'name': 'Gesundheitswesen',
            'slug': 'healthcare',
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
        7: {
            'name': 'Bildung',
            'slug': 'education'
        },
        8: {
            'name': 'Transport',
            'slug': 'transportation'
        },
        9: {
            'name': 'Finanzen',
            'slug': 'financial'
        },
        10: {
            'name': 'Unterhaltung, Kunst & Kultur',
            'slug': 'entertainment'
        },
        0: {
            'name': 'Weiteres',
            'slug': 'misc'
        }
    }

"""
7: {
    'name': 'Bildung',
    'slug': 'education'
},
8: {
    'name': 'Transport',
    'slug': 'transportation'
}
0: {
    'name': 'Weiteres',
    'slug': 'misc'
}
"""