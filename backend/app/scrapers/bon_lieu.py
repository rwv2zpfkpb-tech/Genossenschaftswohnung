"""Scraper fuer die bonlieuGenossenschaft fuer Wohnen und Kultur, Zuerich.

listing_url ist eine sehr alte, statische Snap.js-Seite ohne jede CMS-/
Repeater-Struktur: der Inhalt liegt in zwei `.container.adresse`-Bloecken
innerhalb von `#leftnav` bzw. `.sp75` - handgepflegter Fliesstext, kein
Feld pro Wohnung. Die Genossenschaft vermietet nur 33 Wohnungen in drei
Haeusern (Kochstrasse 2, Sihlfeldstrasse 123, Langstrasse 31), alle in
Zuerich Kreis 4.

Ueber den Wayback-Machine-Verlauf liessen sich 10 Snapshots von Februar 2015
bis Januar 2026 pruefen: in jedem einzelnen stand derselbe Satz "Momentan
sind keine Objekte frei. Wir fuehren keine Anmeldeliste." (rot hervorgehoben)
- in ueber zehn Jahren kein einziger belegter Fall einer echten
Wohnungsausschreibung. Eine strukturierte Feldextraktion (Zimmer/Miete)
laesst sich dadurch nicht gegen echte Daten verifizieren und wird deshalb
bewusst nicht versucht (wie bei `ga_duernten.py`).

Fehlt die Kein-Objekte-frei-Meldung, gehen wir davon aus, dass mindestens
ein Objekt ausgeschrieben ist, und geben den sichtbaren Text des Blocks als
ein einzelnes generisches Inserat zurueck (adresse = Sitz der Genossenschaft)
- genug, um die Notification auszuloesen und eine manuelle Sichtung zu
ermoeglichen.

robots.txt existiert nicht (404), also kein Crawling-Verbot.
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE = re.compile(r"keine\s+Objekte\s+frei", re.IGNORECASE)


class BonLieuScraper(BaseScraper):
    name = "bon_lieu"
    listing_url = "https://www.bonlieu.ch/der-bonlieuwohnbereich.html"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        blocks = page.locator(".container.adresse")
        texts = [
            (await blocks.nth(i).inner_text()).strip()
            for i in range(await blocks.count())
        ]
        texts = [text for text in texts if text]

        full_text = "\n\n".join(texts)
        if not full_text or _NO_VACANCY_RE.search(full_text):
            return []

        return [
            WohnungData(
                genossenschaft=self.name,
                quelle_url=self.listing_url,
                adresse="Kochstrasse 2, 8004 Zürich",
                viertel="Stadt Zürich",
                beschreibung=full_text,
            )
        ]
