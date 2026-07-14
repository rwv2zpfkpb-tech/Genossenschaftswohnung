"""Scraper fuer die Genossenschaft Alterssiedlung Duernten (GAD), Tann ZH.

listing_url ist eine Wix-Seite ohne jede Repeater-/Karten-Struktur: der
gesamte Inhalt besteht aus zwei frei editierbaren Rich-Text-Bloecken
(`[data-testid="richTextElement"]` innerhalb von `<main>`), die das
Vorstandsmitglied von Hand pflegt - kein CMS-Feld pro Wohnung, keine
Detailseiten.

Ueber den Wayback Machine-Verlauf von `/freie-wohnungen` liessen sich 17
Snapshots von Oktober 2020 bis April 2026 pruefen: in jedem einzelnen stand
statt eines Inserats nur eine Kein-Wohnung-frei-Meldung ("Zur Zeit sind
leider keine Wohnungen frei." bis 2022, danach "Momentan ist keine Wohnung
in unsere Siedlung frei!"). Es gibt also in ueber fuenf Jahren keinen einzig
belegten Fall einer echten Wohnungsausschreibung auf dieser Seite - plausibel,
da es sich um eine Alterssiedlung mit entsprechend geringer Fluktuation und
fester Warteliste handelt. Eine strukturierte Feldextraktion (Zimmer/Miete/
Flaeche) laesst sich dadurch prinzipiell nicht gegen echte Daten verifizieren
und wird deshalb bewusst nicht versucht.

Fehlt die Kein-Wohnung-frei-Meldung, gehen wir davon aus, dass mindestens
eine Wohnung ausgeschrieben ist, und geben den gesamten sichtbaren Text der
Rich-Text-Bloecke als ein einzelnes generisches Inserat zurueck (adresse =
Sitz der Siedlung, da einzelne Haus-/Wohnungsnummern im Fliesstext nicht
zuverlaessig zu erkennen sind) - genug, um die Notification auszuloesen und
eine manuelle Sichtung durch den Nutzer zu ermoeglichen.

robots.txt erlaubt uneingeschraenktes Crawlen (nur `?lightbox=`-Query-Links
gesperrt).
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE = re.compile(r"keine\s+Wohnung", re.IGNORECASE)


class GADuerntenScraper(BaseScraper):
    name = "ga_duernten"
    listing_url = "https://www.ga-duernten.ch/freie-wohnungen"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        blocks = page.locator('main [data-testid="richTextElement"]')
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
                adresse="Nauenstrasse 24d, 8632 Tann",
                beschreibung=full_text,
            )
        ]
