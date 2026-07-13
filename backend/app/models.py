"""SQLAlchemy-Modelle."""
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Wohnung(Base):
    """Ein einzelnes Genossenschaftswohnungs-Inserat."""

    __tablename__ = "wohnungen"
    __table_args__ = (UniqueConstraint("quelle_url", name="uq_wohnungen_quelle_url"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Herkunft
    genossenschaft: Mapped[str] = mapped_column(String, index=True)
    quelle_url: Mapped[str] = mapped_column(String, index=True)

    # Objektdaten
    adresse: Mapped[str] = mapped_column(String)
    viertel: Mapped[str | None] = mapped_column(String, nullable=True)
    zimmer: Mapped[float | None] = mapped_column(Float, nullable=True)
    preis: Mapped[int | None] = mapped_column(Integer, nullable=True)
    flaeche: Mapped[float | None] = mapped_column(Float, nullable=True)
    beschreibung: Mapped[str | None] = mapped_column(Text, nullable=True)
    bild_urls: Mapped[list[str]] = mapped_column(JSON, default=list)

    # Geocoding
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Change-Tracking
    hash: Mapped[str] = mapped_column(String)
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ist_aktiv: Mapped[bool] = mapped_column(Boolean, default=True)


class GeocodeCache(Base):
    """Cache fuer Nominatim-Geocoding-Ergebnisse, ein Eintrag pro Adresse.

    lat/lon bleiben null, wenn Nominatim fuer diese Adresse nichts gefunden
    hat - auch das wird gecacht, damit fehlschlagende Adressen nicht bei
    jedem Scraper-Lauf erneut angefragt werden.
    """

    __tablename__ = "geocode_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    adresse: Mapped[str] = mapped_column(String, unique=True, index=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    geocoded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
