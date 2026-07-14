"""Scraper fuer die Stiftung Alterswohnungen der Stadt Zuerich (SAW).

listing_url ist die neue (seit Oktober 2024 aktive) Vermietungs-Plattform
`mieten.wohnenab60.ch/flat` - eine SvelteKit-SPA, server-seitig gerendert.
Es existiert keine `robots.txt` (404), also kein Crawling-Verbot.

Die Seite zeigt unter der Ueberschrift "Freie Wohnungen" eine Grid-Liste
(`div.grid-cols-subgrid`, direkt folgend auf den Wrapper-Div des `<h2>`
"Freie Wohnungen"). Jedes direkte Kind-Div ist eine Karte. Ist keine Wohnung
frei, enthaelt die Liste genau eine Karte mit dem Text
"Aktuell sind keine Wohnungen frei" - Stand Juli 2026 war das durchgehend
der Fall, es gab keine einzige Karte mit echten Inseratsdaten zu verifizieren.

Der serverseitig eingebettete SvelteKit-Datenpayload (`<script>`-Tag) enthaelt
zusaetzlich ein strukturiertes `advertisements`-Array (aktuell leer) sowie ein
`firstRentals`-Array fuer Erstvermietungen von Neubauten (z.B. "Manegghof",
"Espenhof West" - Stand Juli 2026 beide mit laengst abgelaufener
Bewerbungsfrist und nirgends auf der Seite sichtbar gerendert). Da dieses
Firstrentals-Array offenbar unabhaengig vom Bewerbungsfristablauf im Payload
verbleibt, waere ein Parsing dieses Feldes nicht zuverlaessig genug, um
"aktuell aktiv" von "laengst abgelaufen" zu unterscheiden - wir verlassen uns
deshalb bewusst nur auf die sichtbar gerenderten Karten der "Freie
Wohnungen"-Sektion statt auf dieses rohe JS-Objekt.

Da keine echte Wohnungskarte je beobachtet werden konnte, wird bei
vorhandenen Karten (Text weicht vom Kein-Wohnung-frei-Hinweis ab) bewusst
keine Feldextraktion (Zimmer/Miete/Flaeche) versucht, sondern - analog zu
ga_duernten.py - der sichtbare Kartentext als generisches Inserat
zurueckgegeben, inkl. Detail-Link falls die Karte einen enthaelt.
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


class SAWZuerichScraper(BaseScraper):
    name = "saw_zuerich"
    listing_url = "https://mieten.wohnenab60.ch/flat"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="networkidle")

        cards = page.locator(_GRID_XPATH).locator("> div")

        listings: list[WohnungData] = []
        for i in range(await cards.count()):
            card = cards.nth(i)
            text = (await card.inner_text()).strip()
            if not text or _NO_VACANCY_RE.search(text):
                continue

            link = card.locator("a[href]").first
            href = await link.get_attribute("href") if await link.count() else None
            quelle_url = urljoin(self.listing_url, href) if href else self.listing_url
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            adresse = lines[0] if lines else self.listing_url

            listings.append(
                WohnungData(
                    genossenschaft=self.name,
                    quelle_url=quelle_url,
                    adresse=adresse,
                    beschreibung=text,
                )
            )
        return listings
