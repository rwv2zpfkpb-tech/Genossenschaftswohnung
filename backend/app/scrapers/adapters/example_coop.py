"""Vorlage fuer einen Genossenschafts-Adapter.

Kopieren, name/listing_url anpassen und parse() mit den echten
Selektoren der jeweiligen Website fuellen.
"""
from playwright.async_api import Page

from app.scrapers.base import ScrapedListing, ScraperAdapter


class ExampleCoopAdapter(ScraperAdapter):
    name = "example_coop"
    listing_url = "https://example-genossenschaft.ch/wohnungen"

    async def parse(self, page: Page) -> list[ScrapedListing]:
        await page.goto(self.listing_url)

        # TODO: echte Selektoren der Zielseite einsetzen.
        raise NotImplementedError
