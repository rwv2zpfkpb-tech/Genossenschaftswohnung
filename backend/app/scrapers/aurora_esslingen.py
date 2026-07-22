"""Scraper fuer die Baugenossenschaft Aurora, Esslingen ZH.

listing_url ist eine WordPress/WPBakery-Seite. Im Abschnitt `#freie-objekte`
liegen vier `.vcex-icon-box`-Kacheln mit je einer `<h2>`-Ueberschrift
("Objekte", "Groesse und Etage", "Mietzins inkl. Nebenkosten", "Bezug ab") und
optional einem `.vcex-icon-box-content`-Block darunter - offensichtlich ein
von Hand gepflegtes Detailraster fuer die aktuell freien Objekte.

Die "Objekte"-Kachel zeigt im Ruhezustand den Text "Zurzeit keine freie
Objekte"; die uebrigen drei Kacheln haben dann keinen Content-Block. Ueber die
Wayback Machine liess sich nur ein einziger Snapshot der Seite finden (16.
Maerz 2023), der exakt denselben Text zeigt - kein einziger belegter Fall
einer echten Ausschreibung, daher (wie bei `ga_duernten.py`) keine
strukturierte Feldextraktion gegen echte Daten verifizierbar.

Ist die Objekte-Kachel nicht leer/"keine", gehen wir von mindestens einem
ausgeschriebenen Objekt aus und geben den gesamten Text aller vier Kacheln als
ein einzelnes generisches Inserat zurueck (adresse = Sitz der Siedlung gemaess
eingebetteter Google-Maps-Karte: Hotzenwise 1, 8133 Esslingen ZH) - genug, um
die Notification auszuloesen und eine manuelle Sichtung zu ermoeglichen.

robots.txt sperrt nur `/wp-admin/` (mit Ausnahme von admin-ajax.php), die
Siedlungsseite ist uneingeschraenkt crawlbar.
"""
from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper


class AuroraEsslingenScraper(BaseScraper):
    name = "aurora_esslingen"
    listing_url = "https://www.bgaurora.ch/siedlung/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        boxes = page.locator("#freie-objekte .vcex-icon-box")
        fields: dict[str, str] = {}
        for i in range(await boxes.count()):
            box = boxes.nth(i)
            heading_loc = box.locator("h2.vcex-icon-box-heading").first
            if not await heading_loc.count():
                continue
            heading = (await heading_loc.inner_text()).strip()
            content_loc = box.locator(".vcex-icon-box-content").first
            content = (await content_loc.inner_text()).strip() if await content_loc.count() else ""
            fields[heading] = content

        objekte_text = fields.get("Objekte", "")
        if not objekte_text or "keine" in objekte_text.lower():
            return []

        beschreibung = "\n".join(f"{k}: {v}" for k, v in fields.items() if v)
        return [
            WohnungData(
                genossenschaft=self.name,
                quelle_url=self.listing_url,
                adresse="Hotzenwise 1, 8133 Esslingen ZH",
                viertel="Esslingen",
                beschreibung=beschreibung,
            )
        ]
