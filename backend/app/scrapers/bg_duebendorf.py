"""Scraper fuer die Baugenossenschaft Duebendorf.

listing_url ist eine TYPO3-Seite ohne Repeater/Template: pro Liegenschaft mit
aktuellem Angebot gibt es einen `article.grau_unten`-Block mit `<h2>` fuer die
Adresse (Strasse, z.B. "Kriesbachstrasse 65b" - alle Liegenschaften liegen in
Duebendorf) und darunter frei formatiertem HTML (Beschreibung/Konditionen/
Eckdaten als fett hervorgehobene Zwischentitel), von Hand gepflegt und daher
je nach Objekt leicht unterschiedlich strukturiert. Ohne aktuelles Angebot
fehlt der Block komplett (kein "keine Wohnung frei"-Text).

Unter demselben Block-Typ werden auch Parkplaetze/Garagen ausgeschrieben
(aktuell, Stand Juli 2026, steht z.B. nur "Kurvenstrasse 12 - Parkplatz" ohne
"Eckdaten"-Abschnitt); wir ueberspringen jeden Block, dessen Text nicht das
Wort "Wohnung" enthaelt.

Ueber den Wayback-Machine-Verlauf liessen sich mehrere echte Wohnungs-
Ausschreibungen mit dem aktuellen `grau_unten`-Template pruefen (seit
mindestens 2019 unveraendert im Einsatz, z.B. "1.5-Zimmer-Wohnung im 3. OG"
Kriesbachstrasse 65b im September 2019, "3 Zimmer-Wohnung im 1. OG" ebenda im
Dezember 2023) - Zimmerzahl und Mietzins wurden gegen beide Snapshots
verifiziert (1.5 Zimmer/CHF 1'275 bzw. 3 Zimmer/CHF 1'640 Total). Zimmerzahl
steht dabei entweder unter "Eckdaten" als "Zimmer <n>" oder im Titel als
"<n>-Zimmer"/"<n> Zimmer-Wohnung"; der Mietzins steht unter "Konditionen"
meist als "Total: CHF <Betrag>/Monat", vereinzelt (wenn keine Nebenkosten
separat ausgewiesen sind) nur als "Mietzins CHF <Betrag>". Ein Snapshot von
2017 nutzte noch ein anderes Template (kein `grau_unten`) - da das aktuelle
Template seither ueber sieben Jahre stabil war, wird das alte Format nicht
mehr unterstuetzt.

robots.txt existiert nicht (404), also kein Crawling-Verbot.
"""
import re
from urllib.parse import urljoin

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_ROOMS_AFTER_RE = re.compile(r"Zimmer\s+(\d+(?:[.,]\d+)?)", re.IGNORECASE)
_ROOMS_BEFORE_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*Zimmer", re.IGNORECASE)
_TOTAL_PRICE_RE = re.compile(r"Total\D{0,60}CHF\s*([\d'’]+)", re.IGNORECASE)
_MIETZINS_PRICE_RE = re.compile(r"Mietzins\D{0,60}CHF\s*([\d'’]+)", re.IGNORECASE)


class BGDuebendorfScraper(BaseScraper):
    name = "bg_duebendorf"
    listing_url = "https://www.baugenossenschaftduebendorf.ch/liegenschaften/freie-wohnungen/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        blocks = page.locator("article.grau_unten")
        listings: list[WohnungData] = []
        for i in range(await blocks.count()):
            block = blocks.nth(i)
            text = (await block.inner_text()).strip()
            if "wohnung" not in text.lower():
                continue

            link = block.locator("a[href*='/liegenschaften/']").first
            href = await link.get_attribute("href") if await link.count() else None
            quelle_url = urljoin(self.listing_url, href) if href else self.listing_url

            listing = self._parse_listing(text, quelle_url)
            if listing is not None:
                listings.append(listing)
        return listings

    def _parse_listing(self, text: str, quelle_url: str) -> WohnungData | None:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return None
        strasse = lines[0]

        rooms_match = _ROOMS_AFTER_RE.search(text) or _ROOMS_BEFORE_RE.search(text)
        zimmer = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        price_match = _TOTAL_PRICE_RE.search(text) or _MIETZINS_PRICE_RE.search(text)
        preis = int(price_match.group(1).replace("'", "").replace("’", "")) if price_match else None

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=quelle_url,
            adresse=f"{strasse}, 8600 Dübendorf",
            zimmer=zimmer,
            preis=preis,
            beschreibung=text,
        )
