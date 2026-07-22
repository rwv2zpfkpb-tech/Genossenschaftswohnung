"""Scraper fuer die Baugenossenschaft des Eidgenoessischen Personals (BEP), Zuerich.

listing_url ist eine serverseitig gerenderte Contentful-Seite (Bilder liegen
unter `images.ctfassets.net`) ohne jede Repeater-Struktur: der gesamte Inhalt
ist ein einziges `div.bep-content` (in der `.nt`-Spalte - ein zweites
`.bep-content` in der `.ct_r`-Seitenspalte enthaelt nur PDF-Links und wird
ignoriert), von Hand mit `<h2>`-Zwischentiteln gegliedert ("Wohnungen",
"Gewerbeflaechen", "Alle Nebenobjekte", "Ateliers, Studios und zumietbare
Zimmer", "Fahrzeugabstellplaetze"). Wir werten ausschliesslich den Abschnitt
zwischen "Wohnungen" und dem naechsten `<h2>` aus, da die anderen Abschnitte
(v.a. Fahrzeugabstellplaetze) ebenfalls "Mietzins"-Zeilen enthalten und sonst
faelschlich als Wohnungsinserate gezaehlt wuerden.

Jedes Inserat ist ein eigenes `<p>` mit `<br>`-getrennten Zeilen, inkonsistent
beschriftet: Siedlungsname, Zimmerzahl+Stockwerk und Adresse stehen als reiner
Text ohne Label, waehrend Mietzins/Flaeche/Belegung/Mietbeginn ein
"Label: Wert"-Schema verwenden. Eine reine Label-basierte Extraktion wuerde
Siedlung/Zimmer/Adresse verlieren - wir erkennen die Adresszeile deshalb ueber
ein PLZ-Muster (4 Ziffern + Ort) und die Zimmerzeile ueber ein "Zimmer"-Muster,
jeweils nur unter den unbeschrifteten (kein ":") Zeilen, um keine Label-Zeile
(z.B. "Mietbeginn: ... 2026") faelschlich als Adresse zu erkennen.

robots.txt existiert nicht (404 auf bep-zuerich.ch und www.bep-zuerich.ch),
also kein Crawling-Verbot.

Stand Juli 2026 war genau eine Wohnung (Neumuehlestrasse 55, Winterthur-
Neumuehle) ausgeschrieben - Extraktion und Feldnamen sind gegen diese echte
Live-Vakanz verifiziert. Der "keine Wohnung frei"-Wortlaut liess sich mangels
eines beobachtbaren Falls nicht verifizieren; da wir Absaetze ausschliesslich
ueber das Vorkommen von "Mietzins" erkennen, wird ein reiner Fliesstext ohne
Mietzins-Angabe (z.B. eine Kein-Wohnung-frei-Meldung) ohnehin automatisch
uebersprungen.
"""
import html as html_lib
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_TAG_RE = re.compile(r"<[^>]+>")
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_P_RE = re.compile(r"<p>(.*?)</p>", re.IGNORECASE | re.DOTALL)
_SECTION_RE = re.compile(r"<h2>\s*Wohnungen\s*</h2>(.*?)(?:<h2>|$)", re.IGNORECASE | re.DOTALL)

_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)
_ADDRESS_RE = re.compile(r"\d{4}\s+\S")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _clean_html(inner_html: str) -> str:
    text = _TAG_RE.sub("", _BR_RE.sub("\n", inner_html))
    return html_lib.unescape(text)


def _slugify(text: str) -> str:
    text = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return _SLUG_RE.sub("-", text).strip("-") or "wohnung"


class BEPZuerichScraper(BaseScraper):
    name = "bep_zuerich"
    listing_url = "https://www.bep-zuerich.ch/vermietung/freie-objekte/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        content = page.locator(".nt .bep-content").first
        if not await content.count():
            return []
        inner_html = await content.inner_html()

        section_match = _SECTION_RE.search(inner_html)
        if not section_match:
            return []

        listings: list[WohnungData] = []
        for p_html in _P_RE.findall(section_match.group(1)):
            text = _clean_html(p_html)
            if "mietzins" not in text.lower():
                continue
            listing = self._parse_listing(text)
            if listing is not None:
                listings.append(listing)
        return listings

    def _parse_listing(self, text: str) -> WohnungData | None:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        unlabeled = [line for line in lines if ":" not in line]

        fields: dict[str, str] = {}
        for line in lines:
            key, sep, value = line.partition(":")
            if sep:
                fields[key.strip().lower()] = value.strip()

        address = next((line for line in unlabeled if _ADDRESS_RE.search(line)), None)
        if address is None:
            return None

        siedlung = next(
            (line[len("siedlung"):].strip() for line in unlabeled if line.lower().startswith("siedlung")),
            None,
        )

        rooms_match = next(
            (m for line in unlabeled if (m := _ROOMS_RE.search(line))), None
        )
        zimmer = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        price_text = fields.get("mietzins brutto") or fields.get("mietzins") or ""
        price_match = _PRICE_RE.search(price_text)
        preis = int(price_match.group(1).replace("'", "").replace("’", "")) if price_match else None

        area_text = fields.get("fläche") or fields.get("flaeche") or ""
        area_match = _AREA_RE.search(area_text)
        flaeche = float(area_match.group(1).replace(",", ".")) if area_match else None

        identifier = _slugify(siedlung or address)

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=f"{self.listing_url}#{identifier}",
            adresse=address,
            zimmer=zimmer,
            preis=preis,
            flaeche=flaeche,
            beschreibung="\n".join(lines),
        )
