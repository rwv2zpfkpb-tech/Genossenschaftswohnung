"""Scraper fuer die Allgemeine Baugenossenschaft Winterthur (ABW).

Besonderheit dieser Seite: Es gibt keine Uebersicht mit Links auf einzelne
Detailseiten. Freie Wohnungen werden direkt auf listing_url als Eintraege
unter der Ueberschrift "A - Wohnungen" gepflegt (Stand Juli 2026: je ein
<li> in einer <ul>; in aelteren Versionen der Seite - siehe web.archive.org -
war es je ein eigener <h1>-Block). robots.txt erlaubt das Crawlen von
/vermietung/. Da alle Daten bereits auf dieser einen Seite stehen, sind
keine weiteren Requests noetig (kein Delay zwischen Requests erforderlich).

Ohne aktuell freie Wohnung im Live-Betrieb (Stand des letzten Abrufs: keine
Vakanzen) liess sich die Extraktion nicht gegen echte Live-Daten verifizieren,
nur gegen archivierte Snapshots mit realen Inseraten. Bei Format-Aenderungen
der Seite ggf. anpassen.
"""
import hashlib
import re

from playwright.async_api import Locator, Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

#: Textbausteine, mit denen ABW den Platzhalter "keine Wohnung frei" fuellt.
_NO_VACANCY_MARKERS = (
    "werden hier publiziert",
    "zur zeit sind keine",
)

_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"fr\.?\s*([\d'’]+)", re.IGNORECASE)


class ABWWinterthurScraper(BaseScraper):
    name = "abw_winterthur"
    listing_url = "https://abw-winterthur.ch/vermietung/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        wohnungen_liste = page.locator(
            ".entry-content h1:has-text('Wohnungen') ~ ul"
        ).first
        items = wohnungen_liste.locator("> li")

        listings: list[WohnungData] = []
        for i in range(await items.count()):
            listing = await self._parse_item(items.nth(i))
            if listing is not None:
                listings.append(listing)
        return listings

    async def _parse_item(self, item: Locator) -> WohnungData | None:
        text = (await item.inner_text()).strip()
        if not text or any(marker in text.lower() for marker in _NO_VACANCY_MARKERS):
            return None

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        heading = lines[0]
        address = heading.split(",")[0].strip()

        rooms_match = _ROOMS_RE.search(text)
        rooms = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        price_match = _PRICE_RE.search(text)
        price = (
            int(price_match.group(1).replace("'", "").replace("’", ""))
            if price_match
            else None
        )

        image_urls = []
        for img in await item.locator("img").all():
            src = await img.get_attribute("src")
            if src:
                image_urls.append(src)

        first_link = item.locator("a[href]").first
        detail_url = (
            await first_link.get_attribute("href") if await first_link.count() else None
        )
        # Es gibt keine echte Detailseite pro Inserat - falls kein Link
        # vorhanden ist (z.B. kein Grundriss-PDF verlinkt), synthetisieren
        # wir eine stabile, eindeutige URL fuer quelle_url (DB-Unique-Constraint).
        url = detail_url or (
            f"{self.listing_url}#{hashlib.sha1(heading.encode('utf-8')).hexdigest()[:10]}"
        )

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=url,
            adresse=address,
            zimmer=rooms,
            preis=price,
            beschreibung=text,
            bild_urls=image_urls,
        )
