"""Scraper fuer die BUWO - Baugenossenschaft Bubikon/Wolfhausen.

listing_url ist eine Avada/WordPress-Seite (Fusion Builder) ohne echten
Repeater: pro vermieteter Liegenschaft gibt es einen
`.fusion-column-wrapper`-Block mit `<h3>` fuer die vollstaendige Adresse
(Strasse + PLZ/Ort, z.B. "Herschärenstrasse 3a, 8633 Wolfhausen") und darin
einer `ul.fusion-checklist` mit einem `<li>` pro Wohnungseinheit. Jedes `<li>`
enthaelt einen Link auf einen PDF-Vermietungsflyer, dessen Linktext die
Einheit beschreibt (z.B. "3-Zimmer-Wohnung 2. OG rechts") - Miete/Flaeche
stehen nur im PDF, nicht im HTML.

Fehlt eine Ausschreibung, existiert kein solcher Block (kein `<h3>` +
`ul.fusion-checklist`-Paar) unterhalb der "Freie Wohnungen"-Ueberschrift.
Der `<meta name="description">`-Tag der Seite enthaelt zwar den Text "Keine
Freie Wohnungen", das ist aber ein offenbar nie aktualisiertes, statisches
SEO-Feld (identisch bei og:description, unabhaengig vom aktuellen Live-
Angebot) - Erkennung erfolgt deshalb ausschliesslich ueber die tatsaechliche
Blockstruktur im sichtbaren Inhalt, nicht ueber Meta-Tags.

Kein Wayback-Verlauf verfuegbar: die aktuelle Website (Avada-Theme, Bilder ab
2024-03) wurde vom CDX-Crawler nie erfasst, aeltere Snapshots (bis 2018)
zeigen eine komplett andere, laengst abgeloeste Site.

robots.txt erlaubt alles (`Disallow:` ohne Pfad).
"""
import re

from playwright.async_api import Page

from app.crud import WohnungData
from app.scrapers.base import BaseScraper

_ROOMS_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*Zimmer", re.IGNORECASE)


class BUWOBubikonScraper(BaseScraper):
    name = "buwo_bubikon"
    listing_url = "https://buwo.ch/freie-wohnungen/"

    async def scrape(self, page: Page) -> list[WohnungData]:
        await page.goto(self.listing_url, wait_until="load")

        wrappers = page.locator(".post-content .fusion-column-wrapper:has(ul.fusion-checklist)")
        listings: list[WohnungData] = []
        for i in range(await wrappers.count()):
            wrapper = wrappers.nth(i)

            heading = wrapper.locator("h3").first
            adresse = (await heading.inner_text()).strip() if await heading.count() else ""
            if not adresse:
                continue

            intro = wrapper.locator(".fusion-text p").first
            intro_text = (await intro.inner_text()).strip() if await intro.count() else ""

            items = wrapper.locator("ul.fusion-checklist li.fusion-li-item")
            for j in range(await items.count()):
                item = items.nth(j)
                link = item.locator("a").first
                if await link.count():
                    einheit = (await link.inner_text()).strip()
                    href = await link.get_attribute("href")
                    quelle_url = href if href else self.listing_url
                else:
                    einheit = (await item.inner_text()).strip()
                    quelle_url = self.listing_url
                if not einheit:
                    continue

                rooms_match = _ROOMS_RE.search(einheit)
                zimmer = float(rooms_match.group(1).replace(",", ".")) if rooms_match else None

                beschreibung = "\n\n".join(text for text in (intro_text, einheit) if text)

                listings.append(
                    WohnungData(
                        genossenschaft=self.name,
                        quelle_url=quelle_url,
                        adresse=adresse,
                        viertel="Bubikon",
                        zimmer=zimmer,
                        beschreibung=beschreibung,
                    )
                )
        return listings
