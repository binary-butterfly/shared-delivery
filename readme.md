# Shared Delivery / Shop Database

Dieses während #WirVsVirus gestartete Projekt hat zum Ziel, lokale Institutionen wie Wirtschaftsförderungen die
Betreuung der Öffnungszeiten, der Liefer- und der Abhol-möglichkeiten der lokalen Shops während und nach der
Corona-Krise zu ermöglichen.

Hierbei wird als Basis auf OSM-Daten gesetzt. Alle Aktualisierungen müssen ebenfalls unter der ODbL-Lizenz geschehen,
so dass die Daten schlussendlich OpenStreetMap zurückgegeben werden können.

## Installation

Um das System zu installieren, wird Docker und docker-compose empfohlen. Folgende Schritte müssen erledigt werden:

1. Kopieren der config_dist_dev.py zur config.py
2. Ausfüllen der relevanten Parameter:
    1. PROJECT_URL sollte den eigenen Host bekommen
    2. ADMINS sollte die Mailadressen als Liste bekommen, an die Mails gesendet wird
    3. MAILS_FROM sollte den Mail-Absender bekommen
    4. SECRET_KEY sollte einen Zufallsstring bekommen
    5. SECURITY_PASSWORD_SALT sollte ebenfalls einen Zufallsstring bekommen
    6. MAIL_* sollte SMTP-Daten bekommen
    7. MAPBOX_TOKEN sollte einen gültigen Mapbox-Token bekommen
3. Mit `docker-compose build` die Container bauen
4. Mit `docker-compose up` die Container starten
5. Im Kontext des Flask-Containers (z.B. via `docker exec -i -t shared-delivery-flask /bin/bash`) folgende Befehle ausführen:
    1. `python manage.py db upgrade` zum Erstellen der Datenbank
    2. `python manage.py es_create_index` zum Erstellen des ES-Indexes
    3. `python manage.py prepare_unittest` zum Erstellen eines Test-Nutzers. Login ist dann User test@unittest.de, Passwort unittest.