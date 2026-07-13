"""Gemeinsames Interface, das jeder Genossenschafts-Adapter implementiert."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from playwright.async_api import Page


@dataclass
class ScrapedListing:
    """Rohdaten eines Inserats, wie sie ein Adapter aus der Website extrahiert.

    Wird spaeter beim Speichern auf app.models.Listing gemappt.
    """

    external_id: str
    url: str
    title: str
    rooms: float | None = None
    price_chf: float | None = None
    address: str | None = None
    quarter: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ScraperAdapter(ABC):
    """Basisklasse fuer alle Genossenschafts-Scraper.

    Jede Genossenschaft bekommt ein eigenes Modul unter scrapers/adapters/,
    das diese Klasse implementiert. run_scrapers.py iteriert ueber die
    Registry und ruft fuer jeden Adapter parse() auf.
    """

    #: Eindeutiger Kurzname, z.B. "abz", "familienheim_zh" - wird als
    #: Listing.source gespeichert.
    name: str

    #: Startseite mit der Inserate-Uebersicht.
    listing_url: str

    @abstractmethod
    async def parse(self, page: Page) -> list[ScrapedListing]:
        """Laedt listing_url und extrahiert alle aktuell aktiven Inserate.

        Erhaelt eine bereits initialisierte Playwright-Page.
        """
        raise NotImplementedError
