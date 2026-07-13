"""Scraper fuer die Mietergenossenschaft Alpenblick, Horgen.

Alle 14 Wohnungen der Siedlung (Haus A und B, je 7) stehen fest auf einer
einzigen Seite (listing_url, WordPress/Elementor) - es gibt keine
Detailseiten und keine dynamisch nachgeladene Liste. Haus A und Haus B
liegen in zwei separaten, unbenannten Elementor-Top-Level-Sections (nur
Haus A ist zufaellig von einem umgebenden Element mit id="angebot"
eingefasst); ein auf diese id beschraenkter Selektor wuerde Haus B
verschlucken. Die Seite rendert dieselben Daten ausserdem zweimal: als
7-spaltige Tabelle fuer Desktop (Werte ueber mehrere <p> pro Zelle verteilt,
ohne Feldlabel) und als eine Karte pro Wohnung fuer Mobile (ein einzelnes
<p> mit <br>-Trennung: "<strong>Wohnung:</strong> A.1<br><strong>
Aussenbereich:</strong> ...<br><strong>Miete netto:</strong> Vermietet
<br><strong>Nebenkosten:</strong>"). Wir werten nur diese Mobile-Karten aus,
da dort alle Felder eines Inserats in einem Element mit Label stehen.

Wichtig: Die Mobile-Karten sind im Desktop-Viewport (elementor-hidden-desktop)
unsichtbar. Playwright's inner_text() liefert fuer unsichtbare Elemente den
Text ohne die von <br> erzeugten Zeilenumbrueche (alle Felder landen dadurch
unloesbar aneinandergeklebt in einer Zeile) - deshalb wird hier bewusst
inner_html() verwendet und <br> manuell durch Zeilenumbrueche ersetzt, bevor
die uebrigen Tags entfernt werden.

robots.txt erlaubt uneingeschraenktes Crawlen (nur /wp-admin/ gesperrt).

Zum Zeitpunkt der Implementierung (Juli 2026) waren alle 14 Wohnungen mit
"Vermietet" markiert - die Extraktion liess sich daher nicht gegen eine
echte freie Wohnung verifizieren, nur gegen den Vermietet-Fall (0 Treffer,
wie erwartet). Der Grundriss pro Wohnung liegt in einem Popup (Popup Maker),
das strukturell nicht mit der Karte verknuepft ist; wir finden ihn ueber das
Bild-Alt-Attribut, das dem Wohnungscode ohne Punkt entspricht (z.B.
"A.1" -> "A1").
"""
import html as html_lib
import re

from playwright.async_api import Locator, Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_RENTED_MARKER = "vermietet"

_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)


class AlpenblickHorgenScraper(BaseScraper):
    name = "alpenblick_horgen"
    listing_url = "https://alpenblick-horgen.ch/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        paragraphs = page.locator("p")

        listings: list[WohnungData] = []
        for i in range(await paragraphs.count()):
            card = paragraphs.nth(i)
            inner_html = await card.inner_html()
            if "Wohnung:" not in inner_html:
                continue
            listing = await self._parse_card(inner_html, page)
            if listing is not None:
                listings.append(listing)
        return listings

    async def _parse_card(self, inner_html: str, page: Page) -> WohnungData | None:
        text = _TAG_RE.sub("", _BR_RE.sub("\n", inner_html))
        text = html_lib.unescape(text)

        fields: dict[str, str] = {}
        for line in text.splitlines():
            key, sep, value = line.partition(":")
            if sep:
                fields[key.strip().lower()] = value.strip()

        wohnung_id = fields.get("wohnung")
        if not wohnung_id:
            return None

        status = fields.get("miete netto", "")
        if _RENTED_MARKER in status.lower():
            return None

        rooms_match = _NUMBER_RE.search(fields.get("zimmer", ""))
        rooms = float(rooms_match.group(0).replace(",", ".")) if rooms_match else None

        area_match = _NUMBER_RE.search(fields.get("bruttofläche", ""))
        area = float(area_match.group(0).replace(",", ".")) if area_match else None

        price_match = _PRICE_RE.search(status) or _NUMBER_RE.search(status)
        price = (
            int(re.sub(r"[^\d]", "", price_match.group(0)))
            if price_match and re.search(r"\d", price_match.group(0))
            else None
        )

        image_urls: list[str] = []
        floor_plan_alt = wohnung_id.replace(".", "")
        floor_plan_img = page.locator(f'img[alt="{floor_plan_alt}"]').first
        if await floor_plan_img.count():
            src = await floor_plan_img.get_attribute("src")
            if src:
                image_urls.append(src)

        beschreibung = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=f"{self.listing_url}#{wohnung_id}",
            adresse=f"Alpenblick {wohnung_id}, Horgen",
            zimmer=rooms,
            preis=price,
            flaeche=area,
            beschreibung=beschreibung,
            bild_urls=image_urls,
        )
