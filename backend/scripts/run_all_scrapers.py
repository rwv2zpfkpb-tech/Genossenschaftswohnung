"""Einstiegspunkt fuer den GitHub-Actions-Cron-Job.

Startet Playwright, laesst jeden registrierten Adapter parsen, upserted
die Ergebnisse in die DB und verschickt Mail-Benachrichtigungen fuer
neu gefundene Inserate.

Aufruf: python -m scripts.run_scrapers
"""
import asyncio

from playwright.async_api import async_playwright

from app.database import SessionLocal
from app.notifications.mailer import send_new_listing_notification
from app.scrapers.registry import ADAPTERS


async def run_all() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        db = SessionLocal()
        try:
            for adapter_cls in ADAPTERS:
                adapter = adapter_cls()
                scraped = await adapter.parse(page)

                # TODO: scraped Listings mit bestehenden Eintraegen (source,
                # external_id) abgleichen, neue/aktualisierte Zeilen upserten
                # und neu gefundene Inserate sammeln.
                new_listings = []  # type: ignore[var-annotated]

                if new_listings:
                    send_new_listing_notification(new_listings)
        finally:
            db.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run_all())
