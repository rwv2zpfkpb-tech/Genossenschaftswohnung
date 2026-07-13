"""Einstiegspunkt fuer den GitHub-Actions-Cron-Job.

Startet Playwright, fuehrt alle registrierten Scraper nacheinander aus,
upserted die Ergebnisse in die DB und verschickt Mail-Benachrichtigungen fuer
neu gefundene Inserate. Ein fehlschlagender Scraper wird geloggt und
uebersprungen, die restlichen laufen trotzdem weiter. Am Ende wird eine
Zusammenfassung ausgegeben.

Aufruf: python -m scripts.run_all_scrapers
"""
import asyncio
import logging

from playwright.async_api import Page, async_playwright
from sqlalchemy.orm import Session

from app.crud import upsert_wohnung
from app.database import SessionLocal
from app.geocoding import geocode_missing_wohnungen
from app.models import Wohnung
from app.notifications.mailer import send_new_listing_notification
from app.scrapers.base import BaseScraper
from app.scrapers.registry import SCRAPERS

logger = logging.getLogger(__name__)


async def _run_scraper(scraper: BaseScraper, page: Page, db: Session) -> tuple[int, int, list[Wohnung]]:
    """Fuehrt einen Scraper aus und upserted seine Ergebnisse.

    Rueckgabe: (Anzahl neu, Anzahl aktualisiert, neu gefundene Wohnungen).
    """
    neu = 0
    aktualisiert = 0
    neue_wohnungen: list[Wohnung] = []

    for data in await scraper.scrape(page):
        wohnung, ist_neu = upsert_wohnung(db, data)
        if ist_neu:
            neu += 1
            neue_wohnungen.append(wohnung)
        else:
            aktualisiert += 1

    return neu, aktualisiert, neue_wohnungen


async def run_all() -> None:
    logging.basicConfig(level=logging.INFO)

    gesamt_neu = 0
    gesamt_aktualisiert = 0
    fehlgeschlagen: list[str] = []
    alle_neuen_wohnungen: list[Wohnung] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        db = SessionLocal()
        try:
            for scraper_cls in SCRAPERS:
                scraper = scraper_cls()
                try:
                    neu, aktualisiert, neue_wohnungen = await _run_scraper(scraper, page, db)
                except Exception:
                    logger.exception("Scraper '%s' fehlgeschlagen", scraper.name)
                    fehlgeschlagen.append(scraper.name)
                    continue

                gesamt_neu += neu
                gesamt_aktualisiert += aktualisiert
                alle_neuen_wohnungen.extend(neue_wohnungen)

            if alle_neuen_wohnungen:
                send_new_listing_notification(alle_neuen_wohnungen)

            geocodiert = geocode_missing_wohnungen(db)
        finally:
            db.close()
            await browser.close()

    logger.info(
        "Zusammenfassung: %d neu, %d aktualisiert, %d geocodiert, %d Scraper fehlgeschlagen%s",
        gesamt_neu,
        gesamt_aktualisiert,
        geocodiert,
        len(fehlgeschlagen),
        f" ({', '.join(fehlgeschlagen)})" if fehlgeschlagen else "",
    )


if __name__ == "__main__":
    asyncio.run(run_all())
