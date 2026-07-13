"""Geocoding von Wohnungsadressen ueber Nominatim (OpenStreetMap).

Nominatim erlaubt fuer den oeffentlichen Server maximal 1 Request/Sekunde
und verlangt einen identifizierenden User-Agent (siehe
https://operations.osmfoundation.org/policies/nominatim/). Ergebnisse -
auch erfolglose - werden in GeocodeCache gecacht, damit dieselbe Adresse
nie zweimal angefragt wird.
"""
import logging
import time

import requests
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import GeocodeCache, Wohnung

logger = logging.getLogger(__name__)

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_MIN_REQUEST_INTERVAL_SECONDS = 1.0
_REQUEST_TIMEOUT_SECONDS = 10

#: Zeitpunkt (time.monotonic()) des letzten tatsaechlichen Nominatim-Requests,
#: um die 1 req/s-Grenze prozessweit einzuhalten. Cache-Treffer zaehlen nicht.
_last_request_at: float | None = None


def _normalize_address(adresse: str) -> str:
    """Vereinheitlicht eine Adresse als Cache-Key (Whitespace, Gross-/Kleinschreibung)."""
    return " ".join(adresse.split()).lower()


def _respect_rate_limit() -> None:
    global _last_request_at
    if _last_request_at is not None:
        elapsed = time.monotonic() - _last_request_at
        wartezeit = _MIN_REQUEST_INTERVAL_SECONDS - elapsed
        if wartezeit > 0:
            time.sleep(wartezeit)
    _last_request_at = time.monotonic()


def _query_nominatim(adresse: str) -> tuple[float, float] | None:
    """Fragt Nominatim fuer eine einzelne Adresse ab.

    Gibt (lat, lon) zurueck oder None, wenn nichts gefunden wurde oder der
    Request fehlgeschlagen ist. Haelt dabei das 1 req/s-Limit ein.
    """
    settings = get_settings()
    _respect_rate_limit()

    try:
        response = requests.get(
            _NOMINATIM_URL,
            params={"q": adresse, "format": "jsonv2", "limit": 1, "countrycodes": "ch"},
            headers={"User-Agent": settings.nominatim_user_agent},
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        ergebnisse = response.json()
    except (requests.RequestException, ValueError):
        logger.warning("Nominatim-Anfrage fuer Adresse '%s' fehlgeschlagen", adresse, exc_info=True)
        return None

    if not ergebnisse:
        return None

    try:
        return float(ergebnisse[0]["lat"]), float(ergebnisse[0]["lon"])
    except (KeyError, TypeError, ValueError):
        logger.warning("Unerwartete Nominatim-Antwort fuer Adresse '%s': %r", adresse, ergebnisse)
        return None


def geocode(db: Session, adresse: str) -> tuple[float | None, float | None]:
    """Loest eine Adresse zu (lat, lon) auf, mit DB-Cache in GeocodeCache.

    Bereits bekannte Adressen (egal ob erfolgreich oder nicht) werden nicht
    erneut bei Nominatim angefragt.
    """
    cache_key = _normalize_address(adresse)
    cached = db.query(GeocodeCache).filter_by(adresse=cache_key).one_or_none()
    if cached is not None:
        return cached.lat, cached.lon

    treffer = _query_nominatim(adresse)
    lat, lon = treffer if treffer is not None else (None, None)

    db.add(GeocodeCache(adresse=cache_key, lat=lat, lon=lon))
    db.commit()

    return lat, lon


def geocode_missing_wohnungen(db: Session) -> int:
    """Geocodet alle Wohnungen ohne lat/lon anhand ihrer Adresse.

    Schlaegt das Geocoding fuer eine Adresse fehl, bleiben lat/lon einfach
    null - die Wohnung erscheint dann nicht auf der Karte, aber weiterhin
    in der Liste. Gibt die Anzahl erfolgreich geocodeter Wohnungen zurueck.
    """
    wohnungen = db.query(Wohnung).filter(Wohnung.lat.is_(None), Wohnung.lon.is_(None)).all()

    erfolgreich = 0
    for wohnung in wohnungen:
        lat, lon = geocode(db, wohnung.adresse)
        if lat is not None and lon is not None:
            wohnung.lat = lat
            wohnung.lon = lon
            erfolgreich += 1

    db.commit()

    logger.info(
        "Geocoding: %d/%d Wohnungen erfolgreich aufgeloest",
        erfolgreich,
        len(wohnungen),
    )
    return erfolgreich
