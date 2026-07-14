# Scraper-Status

Fortlaufende Arbeitsnotiz: welche Genossenschaften aus
`Genossenschaften_ZH_Inserate_Alle.xlsx` haben bereits einen implementierten
Scraper unter `backend/app/scrapers/`. Bei jedem neuen Scraper diese Datei
aktualisieren (Zeile auf ✅ setzen + Modulname eintragen) und den Stand-Timestamp
unten anpassen.

Stand: 2026-07-14 (9 / 114 implementiert)

## Legende
- ✅ implementiert (in `registry.py` registriert)
- ⬜ offen

| Status | Genossenschaft | Region | Scraper-Modul |
|---|---|---|---|
| ✅ | Allgemeine Baugenossenschaft Winterthur (ABW) | Winterthur | `abw_winterthur.py` |
| ✅ | Allgemeine Baugenossenschaft Zürich (ABZ) | Stadt Zürich | `abz_zuerich.py` |
| ✅ | Alpenblick Horgen | Horgen | `alpenblick_horgen.py` |
| ✅ | Genossenschaft Alte Buchserstrasse Boppelsen | Boppelsen | `buchserstrasse_boppelsen.py` |
| ✅ | Genossenschaft Alterssiedlung Dürnten | Dürnten | `ga_duernten.py` |
| ✅ | Stiftung Alterswohnungen der Stadt Zürich (SAW) | Stadt Zürich | `saw_zuerich.py` |
| ⬜ | Wohngenossenschaft ASIG | Stadt Zürich | |
| ⬜ | Baugenossenschaft Aurora | Esslingen | |
| ⬜ | Wohnbaugenossenschaft Bachtel | Hinwil | |
| ⬜ | Bagestra | Stadt Zürich | |
| ⬜ | Bahoge | Stadt Zürich | |
| ⬜ | Genossenschaft der Baufreunde | Stadt Zürich | |
| ⬜ | Baugenossenschaft des Eidgenössischen Personals (BEP) Zürich | Stadt Zürich | |
| ⬜ | Bon Lieu | Stadt Zürich | |
| ⬜ | Baugenossenschaft Brunnenhof Zürich (BBZ) | Stadt Zürich | |
| ⬜ | BSZ Schönau | Stadt Zürich | |
| ⬜ | Gemeinnützige Baugenossenschaft Burgmatte (GBB) | Stadt Zürich | |
| ⬜ | BUWO - Baugenossenschaft Bubikon/Wolfhausen | Bubikon | |
| ⬜ | Buwo Dübendorf | Dübendorf | |
| ⬜ | Baugenossenschaft Denzlerstrasse Zürich (BDZ) | Stadt Zürich | |
| ⬜ | DOMUM | Winterthur | |
| ⬜ | Baugenossenschaft Dübendorf | Dübendorf | |
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
