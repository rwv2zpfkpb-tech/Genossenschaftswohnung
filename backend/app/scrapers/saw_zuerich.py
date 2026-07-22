"""Scraper fuer die Stiftung Alterswohnungen der Stadt Zuerich (SAW).

listing_url ist die Vermietungs-Plattform `mieten.wohnenab60.ch/flat` - eine
SvelteKit-SPA, server-seitig gerendert. Es existiert keine `robots.txt`
(404), also kein Crawling-Verbot.

Die Seite zeigt unter der Ueberschrift "Freie Wohnungen" eine Grid-Liste
(`div.grid-cols-subgrid`, direkt folgend auf den Wrapper-Div des `<h2>`
"Freie Wohnungen"). Jedes direkte Kind-Div ist eine Karte mit Link auf eine
Detailseite (`/flat/<id>`). Ist keine Wohnung frei, enthaelt die Liste genau
eine Karte mit dem Text "Aktuell sind keine Wohnungen frei".

Stand Juli 2026 waren erstmals drei echte Karten live (vorher durchgehend
keine Vakanz) - damit liess sich die Extraktion gegen echte Daten
verifizieren. Die Karten selbst enthalten nur Zimmerzahl/Titel, Bruttomiete
und die Adresse als reinen Fliesstext (kein Quartier, keine Flaeche); auf der
verlinkten Detailseite steht dagegen eine sauber ausgezeichnete
Definitionsliste ("Details": Siedlung/Adresse/Quartier/Zimmer/Stockwerk/
Flaeche, "Kosten": Bruttomiete/Nettomiete/...) - je ein
`div.flex.items-start.justify-between` mit Label-`<p>` und Werte-`<p
class="...text-right">`. Wir besuchen deshalb pro Karte zusaetzlich die
Detailseite und lesen die Felder darueber aus, statt sie bruechig aus der
Zeilenreihenfolge der Kartenkarte zu raten - bei ueblicherweise 0-3 aktiven
Vakanzen faellt der zusaetzliche Request pro Inserat nicht ins Gewicht.

Der serverseitig eingebettete SvelteKit-Datenpayload (`<script>`-Tag) enthaelt
zusaetzlich ein strukturiertes `advertisements`-Array sowie ein
`firstRentals`-Array fuer Erstvermietungen von Neubauten. Da dieses
Firstrentals-Array offenbar unabhaengig vom Bewerbungsfristablauf im Payload
verbleibt, waere ein Parsing dieses Feldes nicht zuverlaessig genug, um
"aktuell aktiv" von "laengst abgelaufen" zu unterscheiden - wir verlassen uns
deshalb bewusst nur auf die sichtbar gerenderten Karten der "Freie
Wohnungen"-Sektion statt auf dieses rohe JS-Objekt.
"""
import re
from urllib.parse import urljoin

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE = re.compile(r"keine\s+Wohnungen?\s+frei", re.IGNORECASE)

_GRID_XPATH = (
    'xpath=//h2[contains(text(),"Freie Wohnungen")]/ancestor::div[1]'
    '/following-sibling::div[contains(@class,"grid-cols-subgrid")][1]'
)

_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)")
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)


class SAWZuerichScraper(BaseScraper):
    name = "saw_zuerich"
    listing_url = "https://mieten.wohnenab60.ch/flat"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="networkidle")

        cards = page.locator(_GRID_XPATH).locator("> div")

        detail_urls: list[str] = []
        for i in range(await cards.count()):
            card = cards.nth(i)
            text = (await card.inner_text()).strip()
            if not text or _NO_VACANCY_RE.search(text):
                continue

            link = card.locator("a[href]").first
            href = await link.get_attribute("href") if await link.count() else None
            if href:
                detail_urls.append(urljoin(self.listing_url, href))

        listings: list[WohnungData] = []
        for url in detail_urls:
            listing = await self._parse_detail(page, url)
            if listing is not None:
                listings.append(listing)
        return listings

    async def _parse_detail(self, page: Page, url: str) -> WohnungData | None:
        await page.goto(url, wait_until="networkidle")

        adresse = await self._detail_value(page, "Adresse")
        if not adresse:
            return None
        viertel = await self._detail_value(page, "Quartier")

        rooms_match = _ROOMS_RE.search(await self._detail_value(page, "Zimmer") or "")
        zimmer = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        area_match = _AREA_RE.search(await self._detail_value(page, "Fläche") or "")
        flaeche = float(area_match.group(1).replace(",", ".")) if area_match else None

        price_match = _PRICE_RE.search(await self._detail_value(page, "Bruttomiete") or "")
        preis = (
            int(price_match.group(1).replace("'", "").replace("’", ""))
            if price_match
            else None
        )

        beschreibung_locator = page.locator(
            'xpath=//h2[contains(text(),"Beschreibung")]/following-sibling::div[1]//p'
        ).first
        beschreibung = (
            (await beschreibung_locator.inner_text()).strip()
            if await beschreibung_locator.count()
            else None
        )

        image_locator = page.locator('img[alt="Siedlungs Bild"]').first
        bild_urls = []
        if await image_locator.count():
            src = await image_locator.get_attribute("src")
            if src:
                bild_urls.append(urljoin(url, src))

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=url,
            adresse=adresse,
            viertel=viertel,
            zimmer=zimmer,
            preis=preis,
            flaeche=flaeche,
            beschreibung=beschreibung,
            bild_urls=bild_urls,
        )

    async def _detail_value(self, page: Page, label_prefix: str) -> str | None:
        """Liest die Werte-Spalte der "Details"/"Kosten"-Zeile zu einem Label.

        Label und Wert liegen als Geschwister-`<p>` in unterschiedlichen
        Wrapper-Divs innerhalb derselben `justify-between`-Zeile - wir gehen
        vom Label per Ancestor-Achse (Position 1 = naechstgelegener Vorfahr)
        zur Zeile hoch und suchen dort das Werte-`<p>` (`text-right`-Klasse).
        """
        xpath = (
            f'xpath=//p[starts-with(normalize-space(.), "{label_prefix}")]'
            '/ancestor::div[contains(@class,"justify-between")][1]'
            '//p[contains(@class,"text-right")]'
        )
        loc = page.locator(xpath)
        if await loc.count() == 0:
            return None
        return (await loc.first.inner_text()).strip()
