# Genossenschaftswohnungen Zürich

Scraper + Kartenansicht für Genossenschaftswohnungs-Inserate in Zürich.
Findet neue Inserate über mehrere Websites hinweg, benachrichtigt per Mail
und zeigt alle aktiven Inserate mit Filtern (Zimmer, Viertel, Preis) auf
einer Karte an.

Dies ist aktuell nur das Projekt-Skelett — keine Scraper-Logik, keine
Filter-Implementierung, keine Mail-Versand-Logik. Alle TODOs sind im Code
markiert.

## Architektur

```
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────────┐
│  GitHub Actions   │      │      Backend           │      │     Frontend      │
│  Cron (alle 30min)│─────▶│  FastAPI + SQLAlchemy  │◀─────│  React + Leaflet   │
│                  │ ruft │                        │ REST │                  │
│  run_scrapers.py │      │  ┌──────────────────┐  │      │  Kartenansicht +  │
│  ┌────────────┐  │      │  │  Scraper-Adapter   │  │      │  Filterleiste     │
│  │ Playwright │  │─────▶│  │  (ein Modul pro    │  │      └─────────────────┘
│  └────────────┘  │      │  │   Genossenschaft)  │  │
│                  │      │  └──────────────────┘  │
│  Mail-Versand    │      │            │             │
│  bei neuen       │      │            ▼             │
│  Inseraten       │      │  ┌──────────────────┐  │
└─────────────────┘      │  │   Postgres (via    │  │
                          │  │   Supabase)        │  │
                          │  └──────────────────┘  │
                          └──────────────────────┘
```

**Ablauf:**

1. GitHub Actions triggert periodisch `backend/scripts/run_scrapers.py`.
2. Das Script startet Playwright und lässt jeden registrierten Adapter
   (`backend/app/scrapers/adapters/`) die Inserate-Seite seiner
   Genossenschaft parsen. Jeder Adapter implementiert dasselbe Interface
   (`ScraperAdapter.parse(page) -> list[ScrapedListing]`), damit neue
   Genossenschaften ohne Änderungen am Rest des Systems ergänzt werden
   können.
3. Neue/aktualisierte Inserate werden in Postgres (Supabase) upserted.
   Neu gefundene Inserate lösen eine Mail-Benachrichtigung aus.
4. Das Frontend fragt die FastAPI (`GET /listings`) mit Filterparametern
   (Zimmer, Preis, Quartier) ab und zeigt die Treffer auf einer
   Leaflet-Karte an.

## Projektstruktur

```
backend/
  app/
    main.py                  # FastAPI-App, Router-Registrierung
    config.py                 # Settings aus Umgebungsvariablen (.env)
    database.py                # SQLAlchemy Engine/Session
    models.py                  # SQLAlchemy-Modelle (Listing)
    schemas.py                  # Pydantic-Schemas für die API
    api/
      listings.py               # GET /listings mit Filtern
    scrapers/
      base.py                    # ScraperAdapter-Interface + ScrapedListing
      registry.py                 # Liste aller aktiven Adapter
      adapters/
        example_coop.py            # Vorlage für einen neuen Adapter
    notifications/
      mailer.py                    # Mail-Versand bei neuen Inseraten
  scripts/
    run_scrapers.py               # Entrypoint für den Cron-Job
  requirements.txt
  .env.example

frontend/
  src/
    App.jsx                      # Verdrahtet Filter + Karte + API
    components/
      MapView.jsx                 # Leaflet-Karte mit Markern
      FilterPanel.jsx              # Zimmer/Preis/Quartier-Filter
    api/
      client.js                    # fetch-Wrapper fürs Backend
  package.json

.github/workflows/
  scrape.yml                      # Cron-Trigger für run_scrapers.py
```

## Hosting (kostenlos)

- **Datenbank:** [Supabase](https://supabase.com) Free Tier (Postgres).
- **Scraper:** GitHub Actions Cron (im Free-Tier-Limit für private/öffentliche
  Repos ausreichend für einen Lauf alle 30 Minuten).
- **Backend:** z.B. Fly.io / Render Free Tier oder als Supabase Edge
  Function/serverlose Alternative — noch zu entscheiden.
- **Frontend:** statisch, z.B. GitHub Pages, Vercel oder Netlify Free Tier.

## Neuen Genossenschafts-Adapter hinzufügen

1. `backend/app/scrapers/adapters/<name>.py` anlegen, `ScraperAdapter`
   erben, `name`, `listing_url` und `parse()` implementieren.
2. Adapter in `backend/app/scrapers/registry.py` importieren und in
   `ADAPTERS` eintragen.

## Lokale Entwicklung (Grundgerüst)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # Werte anpassen
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
