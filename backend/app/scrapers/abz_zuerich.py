"""Scraper fuer die Allgemeine Baugenossenschaft Zuerich (ABZ).

Freie Mietobjekte werden unter listing_url in einer Card-Liste
(`ul.block-freiemietobjekte__list`) gepflegt - dieselbe Grid-Komponente
("siedlungen"-BEM-Klassen), die die ABZ auch fuer ihre Siedlungsuebersicht
(/bauten/siedlungen/) verwendet. robots.txt erlaubt uneingeschraenktes
Crawlen (Yoast-Block ohne Disallow).

Zum Zeitpunkt der Implementierung (Juli 2026) waren keine Mietobjekte
ausgeschrieben (die Liste ist bei 0 Vakanzen leer im DOM, sowohl serverseitig
gerendert als auch nach dem Laden - kein Nachladen per XHR beobachtet). Auch
in ueber einem Dutzend web.archive.org-Snapshots seit 2020 war die Liste nie
befuellt (Inserate bleiben laut FAQ der Seite oft nur wenige Tage online).
Die Extraktion der Karten-Felder liess sich daher nicht gegen echte Live-Daten
verifizieren - nur die Container-Selektoren (leere Liste) sind bestaetigt.
_parse_item verlaesst sich bewusst auf generische Heuristiken (erste
Ueberschrift/erster Link als Titel, Regex-Suche im Volltext fuer
Zimmer/Preis/Flaeche) statt auf spezifische Card-Klassennamen, damit die
Extraktion auch bei unbekanntem Markup der einzelnen Karten robust bleibt.
Bei der ersten echten Vakanz unbedingt gegen die Live-Seite gegenchecken.
"""
import hashlib
import re

from playwright.async_api import Locator, Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)


class ABZZuerichScraper(BaseScraper):
    name = "abz_zuerich"
    listing_url = "https://www.abz.ch/wohnen/mieten/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        items = page.locator(".block-freiemietobjekte__list > li")

        listings: list[WohnungData] = []
        for i in range(await items.count()):
            listing = await self._parse_item(items.nth(i))
            if listing is not None:
                listings.append(listing)
        return listings

    async def _parse_item(self, item: Locator) -> WohnungData | None:
        text = (await item.inner_text()).strip()
        if not text:
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

        area_match = _AREA_RE.search(text)
        area = float(area_match.group(1).replace(",", ".")) if area_match else None

        image_urls = []
        for img in await item.locator("img").all():
            srcset = await img.get_attribute("data-srcset") or await img.get_attribute(
                "srcset"
            )
            if srcset:
                first_url = srcset.split(",")[0].strip().split(" ")[0]
                if first_url:
                    image_urls.append(first_url)
                continue
            src = await img.get_attribute("data-src") or await img.get_attribute("src")
            if src:
                image_urls.append(src)

        first_link = item.locator("a[href]").first
        detail_url = (
            await first_link.get_attribute("href") if await first_link.count() else None
        )
        url = detail_url or (
            f"{self.listing_url}#{hashlib.sha1(heading.encode('utf-8')).hexdigest()[:10]}"
        )

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=url,
            adresse=address,
            zimmer=rooms,
            preis=price,
            flaeche=area,
            beschreibung=text,
            bild_urls=image_urls,
        )
