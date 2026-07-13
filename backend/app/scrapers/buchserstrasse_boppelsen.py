"""Scraper fuer die Genossenschaft Alte Buchserstrasse Boppelsen ("Wohnen im
Alter", wia-boppelsen.ch).

Die Genossenschaft besitzt eine einzige Liegenschaft (Alte Buchserstrasse 14,
Boppelsen) mit 12 altersgerechten Wohnungen. Es gibt keine Detailseiten und
keine Karten-/Tabellen-Struktur pro Wohnung: freie Wohnungen werden als
Fliesstext in einem einzelnen <p> direkt unter der Ueberschrift
"Freie Wohnungen:" (h3) im .entry-content gepflegt - bei 0 Vakanzen enthaelt
dieses <p> fest den Satz "Zur Zeit sind keine Wohnungen frei.". robots.txt
erlaubt uneingeschraenktes Crawlen (nur /wp-admin/ gesperrt, crawl-delay: 10).

Stand Juli 2026 waren keine Wohnungen frei - die Extraktion des Vakanz-Falls
liess sich daher nicht gegen echte Live-Daten verifizieren, nur der
No-Vacancy-Fall ist bestaetigt. Da mehrere frei werdende Wohnungen im selben
Absatz angekuendigt werden koennten, werten wir <br>-getrennte Zeilen einzeln
aus (analog zu den Mobile-Karten bei alpenblick_horgen.py) und behandeln jede
Zeile mit einer Zimmerangabe als eigenes Inserat; enthaelt keine Zeile eine
Zimmerangabe, aber der Text ist trotzdem kein No-Vacancy-Hinweis, faellt die
Extraktion auf den gesamten Text als ein einzelnes Inserat zurueck, um bei
unbekanntem Format nichts zu verschlucken.
"""
import hashlib
import html as html_lib
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_ADDRESS = "Alte Buchserstrasse 14, Boppelsen"

_NO_VACANCY_MARKER = "keine wohnungen frei"

_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
# Die Genossenschaft schreibt Zimmerzahlen selbst als "3 1/2-Zimmerwohnungen"
# (Leerzeichen + ausgeschriebener Bruch), nicht als "3.5-Zimmer" - siehe die
# Bestandsliste weiter oben auf derselben Seite. Ein einfaches
# "\d+(?:[.,]\d+)?\s*zimmer" wuerde hier faelschlich die "2" aus "1/2" statt
# der "3" davor treffen; deshalb zuerst gezielt auf das Bruch-Format pruefen.
_ROOMS_FRACTION_RE = re.compile(r"(\d+)\s*1/2\s*-?\s*zimmer", re.IGNORECASE)
_ROOMS_DECIMAL_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)


def _parse_rooms(text: str) -> float | None:
    fraction_match = _ROOMS_FRACTION_RE.search(text)
    if fraction_match:
        return float(fraction_match.group(1)) + 0.5
    decimal_match = _ROOMS_DECIMAL_RE.search(text)
    return float(decimal_match.group(1).replace(",", ".")) if decimal_match else None


class BuchserstrasseBoppelsenScraper(BaseScraper):
    name = "buchserstrasse_boppelsen"
    listing_url = "https://wia-boppelsen.ch/wohnungen/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        paragraph = page.locator(
            ".entry-content h3:has-text('Freie Wohnungen') ~ p"
        ).first
        if not await paragraph.count():
            return []

        inner_html = await paragraph.inner_html()
        text = _TAG_RE.sub("", _BR_RE.sub("\n", inner_html))
        text = html_lib.unescape(text).strip()

        if not text or _NO_VACANCY_MARKER in text.lower():
            return []

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        room_lines = [line for line in lines if _parse_rooms(line) is not None]
        entries = room_lines or [text]

        return [self._parse_entry(entry) for entry in entries]

    def _parse_entry(self, entry: str) -> WohnungData:
        rooms = _parse_rooms(entry)

        price_match = _PRICE_RE.search(entry)
        price = (
            int(price_match.group(1).replace("'", "").replace("’", ""))
            if price_match
            else None
        )

        area_match = _AREA_RE.search(entry)
        area = float(area_match.group(1).replace(",", ".")) if area_match else None

        url = f"{self.listing_url}#{hashlib.sha1(entry.encode('utf-8')).hexdigest()[:10]}"

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=url,
            adresse=_ADDRESS,
            zimmer=rooms,
            preis=price,
            flaeche=area,
            beschreibung=entry,
            bild_urls=[],
        )
