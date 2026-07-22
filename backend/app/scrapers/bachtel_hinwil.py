"""Scraper fuer die Wohnbaugenossenschaft Bachtel, Hinwil ZH.

listing_url ist eine Hoststar/Designer-Baukasten-Seite (aehnliches CMS-Muster
wie Duda/Wix, aber eigene Klassen). Der Inhalt zu freien Wohnungen liegt in
einem frei editierbaren `.contentgroup__text-wrapper`-Block, der ueber eine
`<h3>liegenschaften</h3>`-Ueberschrift (`.contentgroup__heading`) identifiziert
wird; direkt danach folgt `.contentgroup__body` mit dem eigentlichen,
handgepflegten Text. Es gibt daneben mehrere weitere contentgroup-Bloecke mit
`<h2>`-Ueberschriften fuer die einzelnen Liegenschaften (Objektbeschreibungen),
die nicht zu freien Wohnungen gehoeren und daher ignoriert werden.

Zwei belegte Snapshots zeigen durchgehend eine Kein-Wohnung-frei-Meldung:
Wayback Machine 29. Mai 2025 ("Zur Zeit gibt es keine freien Wohnungen.") und
der aktuelle Live-Stand Juli 2026 ("Wir haben aktuell keine freien
Wohnungen."). Kein einziger belegter Fall einer echten Ausschreibung, daher
(wie bei `ga_duernten.py`) keine strukturierte Feldextraktion gegen echte
Daten verifizierbar - der Wortlaut der Meldung variiert leicht, das Muster
"keine ... Wohnung" bleibt aber stabil.

Fehlt die Kein-Wohnung-frei-Meldung, gehen wir davon aus, dass mindestens eine
Wohnung ausgeschrieben ist, und geben den gesamten Text des Blocks als ein
einzelnes generisches Inserat zurueck (adresse = Sitz der Genossenschaft
gemaess Impressum: Wihaldenstr. 2, 8340 Hinwil) - genug, um die Notification
auszuloesen und eine manuelle Sichtung zu ermoeglichen.

robots.txt erlaubt Crawling fuer generische User-Agents (`User-agent: *` /
`Allow: /`); gesperrt sind nur namentlich gelistete KI-Bots (u.a. GPTBot,
ClaudeBot), die hier nicht zum Einsatz kommen - Playwright tritt mit
regulaerem Browser-User-Agent auf.
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NO_VACANCY_RE = re.compile(r"keine\s+\S*\s*Wohnung", re.IGNORECASE)


class BachtelHinwilScraper(BaseScraper):
    name = "bachtel_hinwil"
    listing_url = "https://www.wbg-bachtel-hinwil.ch/liegenschaften"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        headings = page.locator(".contentgroup__heading")
        body_text = ""
        for i in range(await headings.count()):
            heading = headings.nth(i)
            heading_text = (await heading.inner_text()).strip().lower()
            if heading_text != "liegenschaften":
                continue
            body = heading.locator(
                "xpath=following-sibling::div[contains(@class,'contentgroup__body')][1]"
            )
            if await body.count():
                body_text = (await body.inner_text()).strip()
            break

        if not body_text or _NO_VACANCY_RE.search(body_text):
            return []

        return [
            WohnungData(
                genossenschaft=self.name,
                quelle_url=self.listing_url,
                adresse="Wihaldenstr. 2, 8340 Hinwil",
                viertel="Hinwil",
                beschreibung=body_text,
            )
        ]
