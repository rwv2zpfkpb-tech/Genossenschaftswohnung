"""Pydantic-Schemas fuer die API."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    url: str
    title: str
    rooms: float | None
    price_chf: float | None
    address: str | None
    quarter: str | None
    latitude: float | None
    longitude: float | None
    first_seen_at: datetime


class ListingFilter(BaseModel):
    """Query-Parameter fuer die Filterung der Kartenansicht."""

    rooms_min: float | None = None
    rooms_max: float | None = None
    price_max: float | None = None
    quarter: str | None = None
