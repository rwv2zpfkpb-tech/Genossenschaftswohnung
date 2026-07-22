"""Scraper fuer die Gemeinnuetzige Baugenossenschaft Burgmatte (GBB), Zuerich.

burgmatte.ch ist eine reine One-Page-Site (keine Unterseiten, robots.txt
liefert 404). Die Vermietungsinfo steckt im Abschnitt `<section id="rent">`
unter der Ueberschrift "Mieten" und besteht nur aus frei formuliertem Text,
kein Repeater mit einzelnen Wohnungs-Karten:

    "Zur Zeit sind leider keine freien Wohnungen verfügbar. Bitte haben Sie
    Verständnis, dass schriftliche und telefonische Anfragen nicht
    beantwortet werden können."
    "Ab nun können keine Anmeldungen entgegen genommen werden."

(Stand Juli 2026, Live-Abruf). Eine strukturierte Feldextraktion laesst sich
ohne echtes Beispiel eines freien Objekts nicht verifizieren und wird bewusst
nicht versucht (wie bei `ga_duernten.py`, `bsz_schoenau.py`). Der Kein-
Wohnung-frei-Text wird per Regex erkannt und fuehrt zu `[]`. Jeder andere
Text im Abschnitt wird als ein einzelnes generisches Inserat zurueckgegeben,
damit ein echter Statuswechsel garantiert die Notification ausloest.
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE = re.compile(
    r"keine\s+freien\s+Wohnungen\s+verf[üu]gbar", re.IGNORECASE
)


class GBBZuerichScraper(BaseScraper):
    name = "gbb_zuerich"
    listing_url = "https://burgmatte.ch/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        section = page.locator("#rent")
        text = (await section.inner_text()).strip() if await section.count() else ""
        if not text or _NO_VACANCY_RE.search(text):
            return []

        return [
            WohnungData(
                genossenschaft=self.name,
                quelle_url=self.listing_url,
                adresse="Karl Stauffer-Strasse 16, 8008 Zürich",
                viertel="Stadt Zürich",
                beschreibung=text,
            )
        ]
