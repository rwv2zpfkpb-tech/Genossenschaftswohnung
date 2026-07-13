"""Schreiboperationen fuer Wohnung-Datensaetze (Upsert-Logik fuer Scraper-Laeufe)."""
import hashlib
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Wohnung

#: Felder, die den Hash bestimmen - alles, was sich bei einer inhaltlichen
#: Aenderung des Inserats aendern wuerde. genossenschaft/quelle_url bewusst
#: aussen vor, da sie die Identitaet des Datensatzes sind, nicht den Inhalt.
_HASH_FIELDS = ("adresse", "viertel", "zimmer", "preis", "beschreibung", "bild_urls")


@dataclass
class WohnungData:
    """Von einem Scraper-Adapter aufbereitete Daten fuer ein Inserat."""

    genossenschaft: str
    quelle_url: str
    adresse: str
    viertel: str | None = None
    zimmer: float | None = None
    preis: int | None = None
    beschreibung: str | None = None
    bild_urls: list[str] = field(default_factory=list)
    lat: float | None = None
    lon: float | None = None


def compute_wohnung_hash(data: WohnungData) -> str:
    """Stabiler Hash ueber die inhaltsrelevanten Felder.

    Damit erkennt upsert_wohnung Aenderungen an einem Inserat, ohne jedes
    Feld einzeln vergleichen zu muessen.
    """
    payload = "|".join(str(getattr(data, feld)) for feld in _HASH_FIELDS)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def upsert_wohnung(db: Session, data: WohnungData) -> tuple[Wohnung, bool]:
    """Legt eine Wohnung an oder aktualisiert sie anhand von quelle_url.

    - quelle_url existiert noch nicht -> neu anlegen.
    - quelle_url existiert, Hash unveraendert -> nur last_seen auffrischen.
    - quelle_url existiert, Hash veraendert -> Felder aktualisieren.

    Rueckgabe: (Wohnung, ist_neu). ist_neu=True steuert die spaetere
    Mail-Benachrichtigung fuer frisch gefundene Inserate.
    """
    neuer_hash = compute_wohnung_hash(data)
    now = datetime.utcnow()

    wohnung = db.query(Wohnung).filter_by(quelle_url=data.quelle_url).one_or_none()

    if wohnung is None:
        wohnung = Wohnung(
            genossenschaft=data.genossenschaft,
            quelle_url=data.quelle_url,
            adresse=data.adresse,
            viertel=data.viertel,
            zimmer=data.zimmer,
            preis=data.preis,
            beschreibung=data.beschreibung,
            bild_urls=data.bild_urls,
            lat=data.lat,
            lon=data.lon,
            hash=neuer_hash,
            first_seen=now,
            last_seen=now,
            ist_aktiv=True,
        )
        db.add(wohnung)
        db.commit()
        db.refresh(wohnung)
        return wohnung, True

    wohnung.last_seen = now
    wohnung.ist_aktiv = True  # erneut gefunden -> wieder online

    if wohnung.hash != neuer_hash:
        wohnung.genossenschaft = data.genossenschaft
        wohnung.adresse = data.adresse
        wohnung.viertel = data.viertel
        wohnung.zimmer = data.zimmer
        wohnung.preis = data.preis
        wohnung.beschreibung = data.beschreibung
        wohnung.bild_urls = data.bild_urls
        wohnung.lat = data.lat
        wohnung.lon = data.lon
        wohnung.hash = neuer_hash

    db.commit()
    db.refresh(wohnung)
    return wohnung, False
