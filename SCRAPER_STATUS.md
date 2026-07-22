# Scraper-Status

Fortlaufende Arbeitsnotiz: welche Genossenschaften aus
`Genossenschaften_ZH_Inserate_Alle.xlsx` haben bereits einen implementierten
Scraper unter `backend/app/scrapers/`. Bei jedem neuen Scraper diese Datei
aktualisieren (Zeile auf ✅ setzen + Modulname eintragen) und den Stand-Timestamp
unten anpassen.

Stand: 2026-07-22 (17 / 114 implementiert)

## Legende
- ✅ implementiert (in `registry.py` registriert)
- ⬜ offen

## Konvention: Genossenschaften ohne aktuell freie Wohnungen

Zeigt eine Genossenschaftsseite im Recherchezeitpunkt (auch über Jahre im
Wayback-Verlauf) durchgehend nur eine "keine Wohnung frei"-Meldung, wird der
Scraper trotzdem gebaut - nicht übersprungen. Muster (siehe `ga_duernten.py`,
`aurora_esslingen.py`, `bachtel_hinwil.py`, `bon_lieu.py`):

- Der Scraper erkennt gezielt den Kein-Wohnung-frei-Text (Regex/String-Check)
  und gibt in diesem Fall `[]` zurück.
- Fehlt dieser Text, wird **nicht** versucht, Zimmer/Miete/Fläche strukturiert
  zu parsen (das lässt sich ohne echtes Beispiel nicht verifizieren). Stattdessen
  wird der gesamte sichtbare Text des betroffenen Blocks als ein einzelnes
  generisches Inserat (`beschreibung` = Rohtext, `adresse` = Sitz der
  Genossenschaft) zurückgegeben.
- Dadurch löst jede echte Ausschreibung garantiert die Notification aus, auch
  wenn die Feldextraktion noch nicht exakt sitzt.
- Taucht danach ein echter Live-Eintrag auf, wird der Scraper anhand dieses
  konkreten Falls nachgeschärft (Regex/Selektoren für Zimmer, Preis etc.
  ergänzen), analog zum Vorgehen bei `bg_duebendorf.py`, wo echte Wayback-
  Snapshots als Referenzdaten genutzt wurden.

| Status | Genossenschaft | Region | Scraper-Modul |
|---|---|---|---|
| ✅ | Allgemeine Baugenossenschaft Winterthur (ABW) | Winterthur | `abw_winterthur.py` |
| ✅ | Allgemeine Baugenossenschaft Zürich (ABZ) | Stadt Zürich | `abz_zuerich.py` |
| ✅ | Alpenblick Horgen | Horgen | `alpenblick_horgen.py` |
| ✅ | Genossenschaft Alte Buchserstrasse Boppelsen | Boppelsen | `buchserstrasse_boppelsen.py` |
| ✅ | Genossenschaft Alterssiedlung Dürnten | Dürnten | `ga_duernten.py` |
| ✅ | Stiftung Alterswohnungen der Stadt Zürich (SAW) | Stadt Zürich | `saw_zuerich.py` |
| ⬜ | Wohngenossenschaft ASIG | Stadt Zürich | |
| ✅ | Baugenossenschaft Aurora | Esslingen | `aurora_esslingen.py` |
| ✅ | Wohnbaugenossenschaft Bachtel | Hinwil | `bachtel_hinwil.py` |
| ⬜ | Bagestra | Stadt Zürich | |
| ⬜ | Bahoge | Stadt Zürich | |
| ⬜ | Genossenschaft der Baufreunde | Stadt Zürich | |
| ✅ | Baugenossenschaft des Eidgenössischen Personals (BEP) Zürich | Stadt Zürich | `bep_zuerich.py` |
| ✅ | Bon Lieu | Stadt Zürich | `bon_lieu.py` |
| ⬜ | Baugenossenschaft Brunnenhof Zürich (BBZ) | Stadt Zürich | |
| ✅ | BSZ Schönau | Stadt Zürich | `bsz_schoenau.py` |
| ✅ | Gemeinnützige Baugenossenschaft Burgmatte (GBB) | Stadt Zürich | `gbb_zuerich.py` |
| ✅ | BUWO - Baugenossenschaft Bubikon/Wolfhausen | Bubikon | `buwo_bubikon.py` |
| ⬜ | Buwo Dübendorf | Dübendorf | |
| ⬜ | Baugenossenschaft Denzlerstrasse Zürich (BDZ) | Stadt Zürich | |
| ⬜ | DOMUM | Winterthur | |
| ✅ | Baugenossenschaft Dübendorf | Dübendorf | `bg_duebendorf.py` |
| ⬜ | Eisenbahner-Baugenossenschaft Zürich-Altstetten (EBA) | Stadt Zürich | |
| ⬜ | EBG Dreispitz | Stadt Zürich | |
| ⬜ | Wohnbaugenossenschaft Effretikon-Illnau | Effretikon + Illnau | |
| ⬜ | Siedlungsgenossenschaft Eigengrund (SGE) | Stadt Zürich | |
| ⬜ | Eisenbahner-Baugenossenschaft Winterthur (EBGW) | Winterthur | |
| ⬜ | Familienheim Genossenschaft Zürich | Stadt Zürich | |
| ⬜ | Baugenossenschaft Freiblick Zürich | Stadt Zürich | |
| ⬜ | Baugenossenschaft Frohes Wohnen | Stadt Zürich | |
| ⬜ | Baugenossenschaft Frohheim (BGF) | Zürich + Winterthur | |
| ⬜ | gaiwo Genossenschaft für Alters- und Invalidenwohnungen | Winterthur | |
| ⬜ | Genossenschaft GASI | Schlieren | |
| ⬜ | Genossenschaft für selbstverwaltetes Wohnen (Gesewo) | Winterthur | |
| ⬜ | Gewobag | Stadt Zürich | |
| ⬜ | Gewomag | Meilen | |
| ⬜ | Gewo Züri Ost | Zürcher Oberland | |
| ⬜ | Baugenossenschaft Gisa | Stadt Zürich | |
| ⬜ | Baugenossenschaft Glattal | Stadt Zürich | |
| ⬜ | Baugenossenschaft Graphika Zürich | Stadt Zürich | |
| ⬜ | Graphis Bau- und Wohngenossenschaft | Stadt Zürich | |
| ⬜ | Habitat 8000 - Stiftung | Zürich + Winterthur | |
| ⬜ | Baugenossenschaft Hagenbrünneli (BGH) | Stadt Zürich | |
| ⬜ | Gemeinnützige Baugenossenschaft Heimelig | Stadt Zürich | |
| ⬜ | Wohngenossenschaft Heimet Adliswil | Adliswil | |
| ⬜ | Heimstätten-Genossenschaft Winterthur (HGW) | Winterthur | |
| ⬜ | Baugenossenschaft Heubach | Horgen | |
| ⬜ | Heugarten | Mönchaltorf | |
| ⬜ | Wohnbaugenossenschaft Holberg | Kloten | |
| ✅ | Bau- und Siedlungsgenossenschaft Höngg (BSH) Zürich | Stadt Zürich | `bsh_zuerich.py` |
| ⬜ | Gemeinnützige Baugenossenschaft Horgen (GBH) | Horgen | |
| ⬜ | IGEBA-Baugenossenschaft Wetzikon | Wetzikon | |
| ⬜ | Wohnstiftung Imfeldsteig für alleinstehende Frauen | Stadt Zürich | |
| ⬜ | Baugenossenschaft Im Michel | Stadt Zürich | |
| ⬜ | Invia Zürich | Stadt Zürich | |
| ⬜ | Kalkbreite | Stadt Zürich | |
| ⬜ | Kleeweid | Stadt Zürich | |
| ⬜ | Kraftwerk 1 - Bau- und Wohngenossenschaft | Stadt Zürich | |
| ⬜ | Baugenossenschaft Kyburg | Stadt Zürich | |
| ⬜ | Baugenossenschaft Letten (BGL) | Stadt Zürich | |
| ✅ | Gemeinnützige Baugenossenschaft Limmattal (GBL) | Stadt Zürich | `gbl_zuerich.py` |
| ⬜ | Baugenossenschaft Linth-Escher | Stadt Zürich | |
| ⬜ | Logis Suisse AG | Zürich + Winterthur | |
| ⬜ | Baugenossenschaft Luegisland | Stadt Zürich | |
| ⬜ | Wohnbaugenossenschaft Maur (WOMA) | Maur | |
| ⬜ | MBGZ | Stadt Zürich | |
| ⬜ | Baugenossenschaft Mehr als Wohnen | Zürich + Winterthur | |
| ⬜ | Mieter-Baugenossenschaft Wädenswil | Wädenswil | |
| ⬜ | Milchbuck Baugenossenschaft | Stadt Zürich | |
| ⬜ | Baugenossenschaft Oberstrass (BGO) | Stadt Zürich | |
| ✅ | PWG - Stiftung | Stadt Zürich | `pwg_zuerich.py` |
| ⬜ | Baugenossenschaft Reppisch Birmensdorf (BRB) | Birmensdorf | |
| ⬜ | Wohnbaugenossenschaft Rüegg | Stadt Zürich | |
| ⬜ | Die Schächli | Dietikon | |
| ⬜ | Baugenossenschaft Schönheim | Stadt Zürich | |
| ⬜ | Wohngenossenschaft Seebrighof | Stadt Zürich | |
| ⬜ | Gemeinnützige Baugenossenschaft Selbsthilfe (GBS) | Stadt Zürich | |
| ⬜ | Siedlungs- und Baugenossenschaft Dübendorf (SBD) | Dübendorf | |
| ⬜ | Baugenossenschaft Sihlhalde | Adliswil + Langnau | |
| ⬜ | Baugenossenschaft SILU | Zürcher Unterland | |
| ⬜ | Genossenschaft Solidus | Winterthur | |
| ⬜ | Genossenschaft Sonnenbühl Uster | Uster | |
| ⬜ | Baugenossenschaft Sonnengarten | Stadt Zürich | |
| ⬜ | Stadt Zürich - Städtische Wohnungen | Stadt Zürich | |
| ⬜ | Dr. Stephan à Porta-Stiftung | Stadt Zürich | |
| ⬜ | Stiftung Einfach Wohnen | Stadt Zürich | |
| ⬜ | Baugenossenschaft St. Jakob (BGSJ) | Stadt Zürich | |
| ⬜ | Baugenossenschaft Süd-Ost | Stadt Zürich | |
| ⬜ | Sunnengarten | Richterswil | |
| ⬜ | Genossenschaft Sunnezirkel | Stadt Zürich | |
| ⬜ | Sunnige Hof | Stadt Zürich | |
| ⬜ | Baugenossenschaft SVEA | Stadt Zürich | |
| ⬜ | Wohnbaugenossenschaft Talgut | Winterthur | |
| ⬜ | Baugenossenschaft Turicum | Stadt Zürich | |
| ⬜ | Bau- und Wohngenossenschaft Uf Dorf | Männedorf + Uetikon | |
| ⬜ | Verein Evangelischer Frauen Zürich (EFZ) | Stadt Zürich | |
| ⬜ | Vitasana Baugenossenschaft | Stadt Zürich | |
| ⬜ | Baugenossenschaft Vrenelisgärtli | Stadt Zürich | |
| ⬜ | Baugenossenschaft Waidberg | Stadt Zürich | |
| ⬜ | Baugenossenschaft Waidmatt (BGW) | Stadt Zürich | |
| ⬜ | Baugenossenschaft Werdmühle | Stadt Zürich | |
| ⬜ | Gemeinnützige Baugenossenschaft Wetzikon (G-B-W) | Wetzikon | |
| ⬜ | Gemeinnützige Wohnbaugenossenschaft Winterthur (GWG) | Winterthur | |
| ⬜ | Wohnsinn Horgen | Horgen | |
| ⬜ | Baugenossenschaft Zentralstrasse | Stadt Zürich | |
| ⬜ | Genossenschaft zum Korn | Stadt Zürich | |
| ⬜ | Zürcher Bau- und Wohngenossenschaft (ZBWG) | Stadt Zürich | |
| ⬜ | Baugenossenschaft Zürich 2 (BGZ2) | Stadt Zürich | |
| ⬜ | Gemeinnützige Baugenossenschaft Zürich 7 (GBZ7) | Stadt Zürich | |
| ⬜ | Gemeinnützige Bau- und Mietergenossenschaft Zürich (GBMZ) | Stadt Zürich | |
| ⬜ | Baugenossenschaft Zürichsee (BGZ) | Küsnacht | |
| ⬜ | Wohn- und Siedlungsgenossenschaft Zürich (WSGZ) | Stadt Zürich | |
| ⬜ | Baugenossenschaft Zürileu | Regensdorf | |
| ⬜ | Zusammenhalt | Winterthur | |

Nicht in der Registry gezaehlt: `example_coop.py` ist eine Vorlage ohne
funktionierende Implementierung (`scrape()` wirft `NotImplementedError`).

## Rechercheergebnisse zu offenen Kandidaten (kein eigener Scraper moeglich)

Bei folgenden Genossenschaften liegen die freien Wohnungen ausschliesslich auf
einem externen Immobilienportal (Homegate/ImmoScout24/eigenes SaaS-Widget)statt
auf einer selbst gehosteten Seite - kein Scraping der Genossenschafts-Website
moeglich, das externe Portal ist entweder botgeschuetzt (Homegate: Cloudflare-
Challenge) oder fachfremd fuer einen Pro-Coop-Scraper:
- Wohngenossenschaft ASIG: asig-wohnen.ch verlinkt nur auf
  homegate.ch/mieten/alle-mietinserate/trefferliste?a=asg (Cloudflare-Schutz).
- Genossenschaft der Baufreunde: baufreunde.ch/vermietung/ bindet ein
  Homegate-Widget ein (`data-provider="homegate"`).
- Baugenossenschaft Brunnenhof Zürich (BBZ): bgbrunnenhof.ch verweist explizit
  auf externe Portale, bindet ein ImmoScout24-Widget ein (`data-provider="is24"`).
- Bagestra: bagestra.ch bindet ein eigenes SaaS-Vermietungsportal
  (vermieten.bagestra.ch, Vite-SPA) per iframe ein.
- Bahoge: bahoge.ch/vermietung/ verlinkt explizit nur auf
  homegate.ch/mieten-oder-kaufen/alle-inserate/trefferliste?a=n134 (Cloudflare-
  Schutz), keine eigene Wohnungsliste auf der Seite.

Wohnbaugenossenschaft Bachtel (Hinwil, wbg-bachtel-hinwil.ch/liegenschaften)
wurde nach demselben Muster wie `ga_duernten.py` umgesetzt (`bachtel_hinwil.py`),
siehe Tabelle oben - dauerhaft "keine freien Wohnungen" (Wayback 29.05.2025
und Live-Stand Juli 2026), bislang kein Fall zum Verifizieren beobachtet.

Baugenossenschaft Aurora (Esslingen, bgaurora.ch/siedlung/#freie-objekte)
wurde nach demselben Muster umgesetzt (`aurora_esslingen.py`), siehe Tabelle
oben.

bonlieuGenossenschaft fuer Wohnen und Kultur (Zuerich Kreis 4,
bonlieu.ch/der-bonlieuwohnbereich.html) wurde nach demselben Muster wie
`ga_duernten.py` umgesetzt (`bon_lieu.py`) - dauerhaft "keine Objekte frei"
(Wayback-Snapshots Februar 2015 bis Januar 2026, alle mit identischem Text),
bislang kein Fall zum Verifizieren beobachtet.

Gemeinnützige Baugenossenschaft Burgmatte (GBB, Zürich Kreis 8, burgmatte.ch)
wurde nach demselben Muster umgesetzt (`gbb_zuerich.py`), siehe Tabelle oben.
Die Seite ist eine reine One-Page-Site (robots.txt liefert 404, keine
Unterseiten); der Abschnitt `#rent` zeigt im Live-Stand Juli 2026 dauerhaft
"Zur Zeit sind leider keine freien Wohnungen verfügbar", bislang kein Fall
zum Verifizieren beobachtet.

BUWO - Baugenossenschaft Bubikon/Wolfhausen (buwo.ch/freie-wohnungen/) wurde
umgesetzt (`buwo_bubikon.py`), siehe Tabelle oben. Die Seite ist eine
Avada/WordPress-Seite (Fusion Builder): pro vermieteter Liegenschaft gibt es
einen Block mit `<h3>`-Adresse und einer `ul.fusion-checklist` mit einem
`<li>` pro Einheit (Linktext auf PDF-Vermietungsflyer, z.B. "3-Zimmer-Wohnung
2. OG rechts") - Miete/Flaeche stehen nur im PDF. Im Live-Stand Juli 2026 war
genau eine Einheit ausgeschrieben (Herschärenstrasse 3a, 8633 Wolfhausen),
gegen die der Scraper verifiziert wurde. Kein Wayback-Verlauf verfuegbar (die
aktuelle Site wurde nie gecrawlt); der `<meta name="description">`-Text
"Keine Freie Wohnungen" ist ein offenbar statisches, nie aktualisiertes
SEO-Feld und wird bewusst nicht zur Erkennung genutzt - stattdessen wird rein
ueber das Vorhandensein von `<h3>` + `ul.fusion-checklist`-Bloecken erkannt.

Baugenossenschaft Schönau (BSZ, Zürich-Seebach, bsz-schoenau.ch/vermietung)
wurde nach demselben Muster umgesetzt (`bsz_schoenau.py`), siehe Tabelle
oben. Besonderheit: der Statustext im `#freie-objekte`-Block wechselt ueber
die Zeit zwischen mehreren Formulierungen (Wayback 2017-2026) - neben zwei
"keine Wohnung frei"-Varianten gab es zwischenzeitlich auch Ankuendigungen
zu einer Neubau-Vermietungsrunde ("~100 neue Wohnungen ab Fruehsommer 2025",
spaeter "Anmeldefenster geschlossen, wir sichten Bewerbungen") - nie aber
eine einzelne Wohnung mit Adresse/Zimmer/Miete. Nur die beiden bekannten
"keine Wohnung frei"-Formulierungen werden per Regex erkannt; jeder andere
Text (inkl. der Vermietungsrunden-Ankuendigungen) loest wie bei `bon_lieu.py`
ein generisches Inserat und damit die Notification aus.
