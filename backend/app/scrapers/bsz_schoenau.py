"""Scraper fuer die Baugenossenschaft Schoenau (BSZ), Zuerich-Seebach.

listing_url ist eine Divi-Builder-Seite (WordPress) ohne Repeater: der
Abschnitt `#freie-objekte` enthaelt statt einzelner Wohnungs-Karten nur einen
einzigen frei formatierten Statustext, den die Genossenschaft von Hand
pflegt. Ueber den Wayback-Machine-Verlauf (2017 bis 2026, siehe unten) wechselt
dieser Text zwischen mehreren Formulierungen, aber alle bisher beobachteten
Snapshots melden entweder "keine Wohnung frei" oder "Bewerbungsfenster
geschlossen/wird gesichtet" - nie eine einzelne Wohnung mit Adresse/Zimmer/
Miete. Eine strukturierte Feldextraktion laesst sich deshalb nicht gegen
echte Daten verifizieren und wird bewusst nicht versucht (wie bei
`ga_duernten.py`).

Beobachtete Formulierungen im Wayback-Verlauf:
- 2017-2023 (mehrfach geprueft, zuletzt 20230127015949): "Momentan stehen
  keine freien Wohnungen zur Verfuegung."
- 2025-01 (20250118162628): Ankuendigung von ~100 Neubauwohnungen, externe
  Vermietung startet Mitte Januar 2025 - kein "keine Wohnung frei"-Text,
  aber auch keine einzelne Wohnung mit Adresse/Zimmer/Miete.
- 2025-03 bis 2025-08 (20250324221318, 20250616091141, 20250810123112):
  "Das Anmeldefenster ... ist geschlossen. Wir sichten aktuell die ...
  Bewerbungen" - ebenfalls kein einzelnes Objekt, aber auch keine der beiden
  "keine Wohnung frei"-Formulierungen unten.
- Seit 2025-10 (20251009072129, 20260116145321, 20260315225959, Live-Stand
  Juli 2026): "Aktuelle sind alle Wohnungen vermietet und wir fuehren keine
  Warteliste."

Beide "keine Wohnung frei"-Formulierungen werden per Regex erkannt und
fuehren zu `[]`. Jeder andere Text (inkl. der Bewerbungsfenster-Meldungen
oben, die auf eine bevorstehende Vermietungsrunde hindeuten) wird - analog
zum Vorgehen bei `bon_lieu.py` - als ein einzelnes generisches Inserat
zurueckgegeben, damit ein echter Statuswechsel garantiert die Notification
ausloest.

robots.txt erlaubt `/vermietung/` (nur `/wp-admin/` und ein Formular-Upload-
Pfad sind gesperrt).
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE_PATTERNS = [
    re.compile(r"keine\s+freien\s+Wohnungen\s+zur\s+Verf[üu]gung", re.IGNORECASE),
    re.compile(r"Wohnungen\s+vermietet\D{0,40}keine\s+Warteliste", re.IGNORECASE),
]


class BSZSchoenauScraper(BaseScraper):
    name = "bsz_schoenau"
    listing_url = "https://www.bsz-schoenau.ch/vermietung/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        section = page.locator("#freie-objekte")
        text = (await section.inner_text()).strip() if await section.count() else ""
        if not text or any(pattern.search(text) for pattern in _NO_VACANCY_RE_PATTERNS):
            return []

        return [
            WohnungData(
                genossenschaft=self.name,
                quelle_url=self.listing_url,
                adresse="Schönauring 65, 8052 Zürich",
                viertel="Stadt Zürich",
                beschreibung=text,
            )
        ]
