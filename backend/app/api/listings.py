"""REST-Endpunkte fuer Inserate (Liste + Filter fuer die Kartenansicht)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ListingOut

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("", response_model=list[ListingOut])
def list_listings(
    rooms_min: float | None = None,
    rooms_max: float | None = None,
    price_max: float | None = None,
    quarter: str | None = None,
    db: Session = Depends(get_db),
) -> list[ListingOut]:
    """Gibt Inserate zurueck, gefiltert nach Zimmerzahl, Preis und Quartier.

    TODO: Filterlogik implementieren (WHERE-Klauseln auf app.models.Listing).
    """
    raise NotImplementedError
