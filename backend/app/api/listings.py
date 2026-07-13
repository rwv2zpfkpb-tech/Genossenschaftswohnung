"""REST-Endpunkte fuer Inserate (Liste + Filter fuer die Kartenansicht)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WohnungOut

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("", response_model=list[WohnungOut])
def list_listings(
    zimmer_min: float | None = None,
    zimmer_max: float | None = None,
    preis_max: int | None = None,
    viertel: str | None = None,
    db: Session = Depends(get_db),
) -> list[WohnungOut]:
    """Gibt Inserate zurueck, gefiltert nach Zimmerzahl, Preis und Viertel.

    TODO: Filterlogik implementieren (WHERE-Klauseln auf app.models.Wohnung).
    """
    raise NotImplementedError
