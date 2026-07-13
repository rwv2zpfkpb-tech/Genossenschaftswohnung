"""REST-Endpunkte fuer Inserate (Liste + Filter fuer die Kartenansicht)."""
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Wohnung
from app.schemas import WohnungFilter, WohnungOut

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("", response_model=list[WohnungOut])
def list_listings(
    filters: WohnungFilter = Depends(),
    db: Session = Depends(get_db),
) -> list[WohnungOut]:
    """Gibt aktive Inserate zurueck, gefiltert nach Zimmerzahl, Preis, Flaeche und Viertel.

    Inserate ohne Wert fuer ein Feld werden von dessen Filter nicht
    ausgeschlossen (z.B. eine Wohnung ohne bekannte Zimmerzahl bleibt trotz
    zimmer_min in der Ergebnismenge) - Unbekannt heisst nicht Unpassend.
    """
    query = db.query(Wohnung).filter(Wohnung.ist_aktiv.is_(True))

    if filters.zimmer_min is not None:
        query = query.filter(or_(Wohnung.zimmer.is_(None), Wohnung.zimmer >= filters.zimmer_min))
    if filters.zimmer_max is not None:
        query = query.filter(or_(Wohnung.zimmer.is_(None), Wohnung.zimmer <= filters.zimmer_max))
    if filters.preis_max is not None:
        query = query.filter(or_(Wohnung.preis.is_(None), Wohnung.preis <= filters.preis_max))
    if filters.flaeche_max is not None:
        query = query.filter(or_(Wohnung.flaeche.is_(None), Wohnung.flaeche <= filters.flaeche_max))
    if filters.viertel is not None:
        query = query.filter(Wohnung.viertel == filters.viertel)

    return query.order_by(Wohnung.first_seen.desc()).all()
