"""Scraper fuer die Gemeinnuetzige Baugenossenschaft Limmattal (GBL), Zuerich.

Anders als bei allen bisherigen Scrapern hat die GBL keine eigene
Inserate-Seite: laut `/freie-objekte.php` auf gbl.ch werden saemtliche freien
Wohnungen ausschliesslich auf dem Immobilienportal Flatfox
(flatfox.ch/de/gbl/listings/) ausgeschrieben. Diese Flatfox-Suchseite ist eine
JS-Single-Page-Anwendung (ffbl-Such-Widget), die ihre Daten von der
oeffentlichen, unauthentifizierten Flatfox-API laedt. Wir rufen diese API
direkt per requests auf (kein Playwright/HTML-Parsing noetig) - robots.txt von
flatfox.ch erlaubt `/api/` uneingeschraenkt (nur /admin/, /*/partner/ u.ae.
gesperrt).

Die GBL-Organisation hat auf Flatfox die stabile numerische ID 729 (aus dem
eingebetteten `organizationPk` auf der Listings-Seite). Die API liefert unter
`/api/v1/public-listing/?organization=729` paginierte, bereits vollstaendig
strukturierte Listing-Objekte (Adresse, Zimmerzahl, Miete, Flaeche,
Beschreibung, Bilder) - eine eigene Text-Extraktion per Regex entfaellt hier
komplett. Wir filtern zusaetzlich auf offer_type=RENT und
object_category=APARTMENT, da Genossenschaften auf Flatfox teilweise auch
Parkplaetze/Lagerraum/Verkaufsobjekte inserieren.

Stand Juli 2026 war genau eine Wohnung (Muehlezelgstrasse 16, Zuerich-
Albisrieden) ausgeschrieben - Extraktion und Feldnamen sind gegen diese echte
Live-Vakanz verifiziert (die numerischen Werte des Inserats aenderten sich
waehrend der Implementierung mehrfach - vermutlich Live-Korrekturen durch die
GBL selbst - das ist kein Extraktionsfehler). Die Pagination (`next`-URL,
Standard-DRF-Schema) liess sich mangels eines zweiten Ergebnisses nicht gegen
echte Mehrseiten-Daten verifizieren.
"""
import requests
from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_ORGANIZATION_ID = 729
_API_URL = "https://flatfox.ch/api/v1/public-listing/"
_BASE_URL = "https://flatfox.ch"


class GBLZuerichScraper(BaseScraper):
    name = "gbl_zuerich"
    listing_url = "https://flatfox.ch/de/gbl/listings/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        listings: list[WohnungData] = []
        url: str | None = _API_URL
        params: dict[str, object] | None = {
            "organization": _ORGANIZATION_ID,
            "offer_type": "RENT",
            "object_category": "APARTMENT",
            "expand": "images",
            "limit": 50,
        }
        while url:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            listings.extend(self._parse_item(item) for item in data["results"])
            url = data.get("next")
            params = None  # "next" ist bereits eine vollstaendige URL

        return listings

    def _parse_item(self, item: dict) -> WohnungData:
        rooms_raw = item.get("number_of_rooms")
        rooms = float(rooms_raw) if rooms_raw not in (None, "") else None

        area = item.get("surface_living")

        beschreibung = "\n\n".join(
            part for part in (item.get("description_title"), item.get("description")) if part
        )

        image_urls = [
            f"{_BASE_URL}{image['url']}"
            for image in item.get("images", [])
            if image.get("url")
        ]

        return WohnungData(
            genossenschaft=self.name,
            quelle_url=f"{_BASE_URL}{item['url']}",
            adresse=item.get("public_address", ""),
            zimmer=rooms,
            preis=item.get("price_display"),
            flaeche=float(area) if area is not None else None,
            beschreibung=beschreibung,
            bild_urls=image_urls,
        )
