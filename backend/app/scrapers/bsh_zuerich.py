"""Scraper fuer die Bau- und Siedlungsgenossenschaft Hoengg (BSH), Zuerich.

Anders als bei allen anderen bisherigen Scrapern stehen die Inserate nicht
als HTML-Karten auf listing_url, sondern als einzelne PDF-Flyer. Die
eigentliche Seite `/freie-wohnungen/` enthaelt keine Liste, sondern nur einen
Link auf die Downloads-Seite ("Hier finden Sie die aktuelle Auflistung der
freien Wohnungen."); wir scrapen deshalb direkt `/downloads/`. robots.txt
erlaubt uneingeschraenktes Crawlen (nur /wp-admin/ gesperrt, crawl-delay: 10).

Auf `/downloads/` steht unter der Ueberschrift "Vermietung Wohnungen und
weitere Objekte" eine `<ul class="fusion-checklist">` mit je einem Link pro
ausgeschriebenem Objekt (PDF). Der Ueberschriftentext liegt in
`<h3><p id="anchorContent" class="page_title">...</p></h3>` - die Liste
selbst ist keine Geschwisterin von `<p>` oder `<h3>`, sondern vom
umschliessenden `div.fusion-title`. Wir suchen daher gezielt nach diesem
`<p class="page_title">` und nehmen von dessen Vorfahren-`div.fusion-title`
die naechste `ul.fusion-checklist`-Geschwisterliste.

Unter derselben Ueberschrift landen auch Nicht-Wohnungs-Objekte (Garagen/
Parkplaetze/Kellerabteile); wir filtern anhand des Linktitels alles heraus,
was nach einem dieser Objekttypen klingt.

Jeder PDF-Flyer folgt demselben Formular-Template (bestaetigt anhand von
zwei aktuell ausgeschriebenen Garagen-Flyern, Stand Juli 2026 - eine echte
Wohnung war zum Zeitpunkt der Implementierung nicht ausgeschrieben, die
Extraktion der Wohnungs-spezifischen Felder Zimmer/Flaeche liess sich daher
nicht gegen echte Live-Daten verifizieren):

    Ref.-Nr. <id>
    <Titel/Objektbezeichnung>
    <Adresse>, <PLZ Ort>

    Nettomiete:  CHF  <Betrag>

    Verfuegbar:  <Text>

    Bewerbungsfrist  <Text>

Wir laden den Flyer per `requests` herunter (kein Playwright noetig fuer ein
PDF) und extrahieren den Text mit `pypdf`.
"""
import io
import re

import pypdf
import requests
from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_NON_WOHNUNG_KEYWORDS = (
    "garage",
    "parkplatz",
    "motorrad",
    "abstellplatz",
    "keller",
    "lagerraum",
)

_REF_RE = re.compile(r"Ref\.?-?Nr\.?\s*(\S+)", re.IGNORECASE)
_LABEL_LINE_RE = re.compile(
    r"^(Nettomiete|Bruttomiete|Nebenkosten|Zimmer|Fl(?:ä|ae)che|Wohnfl(?:ä|ae)che|"
    r"Verf(?:ü|ue)gbar|Bewerbungsfrist)",
    re.IGNORECASE,
)
_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)
#: Siehe gbl_zuerich.py - ohne browserartigen User-Agent blocken manche WAFs
#: requests.get() (haeufig mit einer leeren statt einer Fehler-Antwort).
_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}


class BSHZuerichScraper(BaseScraper):
    name = "bsh_zuerich"
    listing_url = "https://bsh-zuerich.ch/downloads/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        heading = page.locator(
            "p.page_title", has_text="Vermietung Wohnungen und weitere Objekte"
        ).first
        checklist = heading.locator(
            "xpath=ancestor::div[contains(@class,'fusion-title')][1]"
            "/following-sibling::ul[contains(@class,'fusion-checklist')][1]"
        )
        links = checklist.locator("a[href]")

        objekte: list[tuple[str, str]] = []
        for i in range(await links.count()):
            link = links.nth(i)
            href = await link.get_attribute("href")
            titel = (await link.inner_text()).strip()
            if href and titel:
                objekte.append((href, titel))

        listings: list[WohnungData] = []
        for href, titel in objekte:
            if any(keyword in titel.lower() for keyword in _NON_WOHNUNG_KEYWORDS):
                continue
            listing = self._parse_pdf(href, titel)
            if listing is not None:
                listings.append(listing)
        return listings

    def _parse_pdf(self, url: str, titel: str) -> WohnungData | None:
        response = requests.get(url, headers=_HEADERS, timeout=30)
        response.raise_for_status()
        reader = pypdf.PdfReader(io.BytesIO(response.content))
        text = "\n".join(pdf_page.extract_text() or "" for pdf_page in reader.pages)

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return None

        start = 0
        for i, line in enumerate(lines):
            if _REF_RE.match(line):
                start = i + 1
                break

        header_lines: list[str] = []
        for line in lines[start:]:
            if _LABEL_LINE_RE.match(line):
                break
            header_lines.append(line)
        address = header_lines[-1] if header_lines else titel

        rooms_match = _ROOMS_RE.search(text)
        rooms = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        price_match = _PRICE_RE.search(text)
        price = (
            int(price_match.group(1).replace("'", "").replace("’", ""))
            if price_match
            else None
        )

        area_match = _AREA_RE.search(text)
        area = float(area_match.group(1).replace(",", ".")) if area_match else None

        beschreibung = "\n".join(lines)

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=url,
            adresse=address,
            zimmer=rooms,
            preis=price,
            flaeche=area,
            beschreibung=beschreibung,
            bild_urls=[],
        )
