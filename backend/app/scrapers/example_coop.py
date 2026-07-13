"""Vorlage fuer einen Genossenschafts-Scraper.

Kopieren, name/listing_url anpassen und scrape() mit den echten
Selektoren der jeweiligen Website fuellen.
"""
from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper


class ExampleCoopScraper(BaseScraper):
    name = "example_coop"
    listing_url = "https://example-genossenschaft.ch/wohnungen"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url)

        # TODO: echte Selektoren der Zielseite einsetzen.
        raise NotImplementedError
