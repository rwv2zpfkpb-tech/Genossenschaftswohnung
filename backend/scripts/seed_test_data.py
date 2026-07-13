"""Legt eine Test-Genossenschaft mit Test-Inseraten an (End-to-End-Test der
Pipeline DB -> API -> Frontend/Karte), ohne auf einen echten Scraper-Fund zu
warten.

Nutzt dieselbe upsert_wohnung()-Logik wie ein echter Scraper-Lauf, ist aber
NICHT in scrapers/registry.py eingetragen und laeuft daher nie automatisch
im Cron-Job mit. genossenschaft="test_coop" und quelle_url unter der
reservierten .invalid-Domain (RFC 2606) markieren die Datensaetze eindeutig
als Testdaten.

Aufruf (aus backend/, mit aktivierter venv und passender .env):
    python -m scripts.seed_test_data           # Testdaten anlegen/aktualisieren
    python -m scripts.seed_test_data --remove   # Testdaten wieder entfernen
"""
import argparse
import logging

from app.crud import WohnungData, upsert_wohnung
from app.database import SessionLocal
from app.models import Wohnung

logger = logging.getLogger(__name__)

GENOSSENSCHAFT = "test_coop"
_BESCHREIBUNG = (
    "TESTDATEN - generiert zum Testen der Kartenansicht. "
    "Sicher loeschbar via: python -m scripts.seed_test_data --remove"
)

_TEST_LISTINGS = [
    WohnungData(
        genossenschaft=GENOSSENSCHAFT,
        quelle_url="https://test-genossenschaft.invalid/inserat/1",
        adresse="Testweg 1, 8001 Zürich",
        viertel="Altstadt",
        zimmer=2.5,
        preis=1450,
        flaeche=55,
        beschreibung=_BESCHREIBUNG,
        lat=47.3728,
        lon=8.5411,
    ),
    WohnungData(
        genossenschaft=GENOSSENSCHAFT,
        quelle_url="https://test-genossenschaft.invalid/inserat/2",
        adresse="Teststrasse 22, 8003 Zürich",
        viertel="Wiedikon",
        zimmer=3.5,
        preis=1890,
        flaeche=78,
        beschreibung=_BESCHREIBUNG,
        lat=47.3703,
        lon=8.5183,
    ),
    WohnungData(
        genossenschaft=GENOSSENSCHAFT,
        quelle_url="https://test-genossenschaft.invalid/inserat/3",
        adresse="Musterplatz 5, 8006 Zürich",
        viertel="Unterstrass",
        zimmer=1.5,
        preis=990,
        flaeche=34,
        beschreibung=_BESCHREIBUNG,
        lat=47.3897,
        lon=8.5442,
    ),
    WohnungData(
        genossenschaft=GENOSSENSCHAFT,
        quelle_url="https://test-genossenschaft.invalid/inserat/4",
        adresse="Beispielgasse 9, 8047 Zürich",
        viertel="Albisrieden",
        zimmer=4.5,
        preis=2350,
        flaeche=102,
        beschreibung=_BESCHREIBUNG,
        lat=47.3789,
        lon=8.4869,
    ),
    WohnungData(
        genossenschaft=GENOSSENSCHAFT,
        quelle_url="https://test-genossenschaft.invalid/inserat/5",
        adresse="Probeweg 3, 8038 Zürich",
        viertel="Wollishofen",
        zimmer=5.5,
        preis=2890,
        flaeche=130,
        beschreibung=_BESCHREIBUNG,
        lat=47.3407,
        lon=8.5309,
    ),
]


def seed() -> None:
    db = SessionLocal()
    try:
        for data in _TEST_LISTINGS:
            wohnung, ist_neu = upsert_wohnung(db, data)
            logger.info("%s: %s (id=%d)", "neu" if ist_neu else "aktualisiert", wohnung.adresse, wohnung.id)
    finally:
        db.close()


def remove() -> None:
    db = SessionLocal()
    try:
        geloescht = db.query(Wohnung).filter(Wohnung.genossenschaft == GENOSSENSCHAFT).delete()
        db.commit()
        logger.info("%d Test-Inserate entfernt", geloescht)
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove", action="store_true", help="Testdaten wieder entfernen statt anlegen")
    args = parser.parse_args()
    remove() if args.remove else seed()
