"""Gemeinsames Interface, das jeder Genossenschafts-Scraper implementiert."""
from abc import ABC, abstractmethod

from playwright.async_api import Page

from app.crud import WohnungData


class BaseScraper(ABC):
    """Basisklasse fuer alle Genossenschafts-Scraper.

    Jede Genossenschaft bekommt ein eigenes Modul unter scrapers/, das diese
    Klasse implementiert. run_all_scrapers.py iteriert ueber die Registry und
    ruft fuer jeden Scraper scrape() auf.
    """

    #: Eindeutiger Kurzname, z.B. "abz", "familienheim_zh" - wird als
    #: Wohnung.genossenschaft gespeichert.
    name: str

    #: Startseite mit der Inserate-Uebersicht.
    listing_url: str

    @abstractmethod
    async def scrape(self, page: Page) -> list[WohnungData]:
        """Laedt listing_url und extrahiert alle aktuell aktiven Inserate.

        Erhaelt eine bereits initialisierte Playwright-Page. Gibt bereits
        fertig aufbereitete WohnungData zurueck (genossenschaft = self.name).
        """
        raise NotImplementedError
