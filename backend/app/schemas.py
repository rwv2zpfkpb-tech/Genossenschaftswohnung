"""Pydantic-Schemas fuer die API."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WohnungOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    genossenschaft: str
    quelle_url: str
    adresse: str
    viertel: str | None
    zimmer: float | None
    preis: int | None
    beschreibung: str | None
    bild_urls: list[str]
    lat: float | None
    lon: float | None
    first_seen: datetime


class WohnungFilter(BaseModel):
    """Query-Parameter fuer die Filterung der Kartenansicht."""

    zimmer_min: float | None = None
    zimmer_max: float | None = None
    preis_max: int | None = None
    viertel: str | None = None
