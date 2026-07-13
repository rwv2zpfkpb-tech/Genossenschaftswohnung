"""Scraper fuer die Stiftung PWG, Zuerich (pwg.ch).

Alle Mietobjekte (Wohnungen, Gewerbe, aber auch Parkplaetze/Garagen/Keller)
stehen serverseitig gerendert auf einer einzigen Seite
(`/liegenschaften/zu-vermieten`, TYPO3) als Liste von
`.liegenschaften-item-vermieten`-Containern - keine Paginierung, kein
Nachladen per JS beobachtet (curl ohne JS liefert bereits alle Karten).
robots.txt erlaubt uneingeschraenktes Crawlen dieser Seite (nur /typo3/ und
Export-Pfade gesperrt).

Jeder Container traegt `data-category` ("hauptobjekt" fuer Wohnung/Gewerbe,
"nebenobjekt" fuer Parkplaetze/Garagen/Keller/Motorradplaetze). Da diese App
Wohnungs-Inserate sammelt, filtern wir zusaetzlich auf das sichtbare
Kategorie-Label ".category" == "Wohnung" und ueberspringen Gewerbe- sowie
alle Nebenobjekt-Karten.

Die Kurzbeschreibung + Detail-Tabelle (Nettomiete/Nebenkosten/Bruttomiete,
Verfuegbar ab) liegt in einer Akkordeon-Sektion (`.row2.more-info`), die per
CSS bis zum Klick auf "Weitere Informationen anzeigen" ausgeblendet ist -
analog zu den Mobile-Karten bei alpenblick_horgen.py lesen wir hier bewusst
inner_html() statt inner_text(), da Playwright fuer unsichtbare Elemente
sonst leeren Text liefert.

Als quelle_url wird die UUID aus dem "Jetzt bewerben!"-Link
(melon.rent-Bewerbungsformular, `?uuids=<uuid>`) verwendet: sie ist pro
Mietobjekt stabil, waehrend die Position/ID (`#item-N`) der Karte auf der
Seite von der Gesamtzahl aller (auch nicht erfassten Nebenobjekt-)Inserate
abhaengt und sich bei jeder Aenderung verschieben kann - fuer
upsert_wohnung() (matched ueber quelle_url) waere das fatal.

Stand Juli 2026 war genau eine Wohnung (Baslerstrasse 105, Zuerich-Altstetten)
ausgeschrieben - die Extraktion ist gegen diese echte Live-Vakanz verifiziert.
"""
import html as html_lib
import re
from urllib.parse import urljoin

from playwright.async_api import Locator, Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_TAG_RE = re.compile(r"<[^>]+>")
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*zimmer", re.IGNORECASE)
_PRICE_RE = re.compile(r"(?:fr\.?|chf)\s*([\d'’]+)", re.IGNORECASE)
_AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:2|²)", re.IGNORECASE)
_UUID_RE = re.compile(r"uuids=([\w-]+)")


def _clean_html(inner_html: str) -> str:
    text = _TAG_RE.sub("", _BR_RE.sub("\n", inner_html))
    return html_lib.unescape(text)


class PWGZuerichScraper(BaseScraper):
    name = "pwg_zuerich"
    listing_url = "https://www.pwg.ch/liegenschaften/zu-vermieten"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        items = page.locator(".liegenschaften-item-vermieten")

        listings: list[WohnungData] = []
        for i in range(await items.count()):
            listing = await self._parse_item(items.nth(i))
            if listing is not None:
                listings.append(listing)
        return listings

    async def _parse_item(self, item: Locator) -> WohnungData | None:
        category_locator = item.locator(".category").first
        if not await category_locator.count():
            return None
        category_text = _clean_html(await category_locator.inner_html()).strip()
        if not category_text.lower().startswith("wohnung"):
            return None

        titel_locator = item.locator(".titel").first
        titel = (await titel_locator.inner_text()).strip() if await titel_locator.count() else ""

        address_locator = item.locator(".adresse").first
        address_lines = _clean_html(await address_locator.inner_html()).splitlines()
        address = ", ".join(line.strip() for line in address_lines if line.strip())

        rooms_locator = item.locator(".rooms").first
        rooms_text = await rooms_locator.inner_text() if await rooms_locator.count() else ""
        rooms_match = _ROOMS_RE.search(rooms_text)
        rooms = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

        price_locator = item.locator(".prize").first
        price_text = await price_locator.inner_text() if await price_locator.count() else ""
        price_match = _PRICE_RE.search(price_text)
        price = (
            int(price_match.group(1).replace("'", "").replace("’", ""))
            if price_match
            else None
        )

        area_locator = item.locator(".area").first
        area_text = await area_locator.inner_text() if await area_locator.count() else ""
        area_match = _AREA_RE.search(area_text)
        area = float(area_match.group(1).replace(",", ".")) if area_match else None

        move_in_locator = item.locator(".move_in_date").first
        move_in = (
            (await move_in_locator.inner_text()).strip()
            if await move_in_locator.count()
            else ""
        )

        more_info_locator = item.locator(".row2.more-info .col1").first
        more_info = (
            _clean_html(await more_info_locator.inner_html()).strip()
            if await more_info_locator.count()
            else ""
        )

        beschreibung = "\n\n".join(
            part for part in (titel, move_in, more_info) if part
        )

        image_urls = []
        for img in await item.locator(".liegenschaft-img-wrapper img").all():
            src = await img.get_attribute("src")
            if src:
                image_urls.append(urljoin(self.listing_url, src))

        apply_locator = item.locator("a.button-vermieten").first
        apply_href = (
            await apply_locator.get_attribute("href")
            if await apply_locator.count()
            else None
        )
        uuid_match = _UUID_RE.search(apply_href or "")
        identifier = uuid_match.group(1) if uuid_match else None
        if identifier is None:
            return None

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=f"{self.listing_url}#{identifier}",
            adresse=address,
            zimmer=rooms,
            preis=price,
            flaeche=area,
            beschreibung=beschreibung,
            bild_urls=image_urls,
        )
