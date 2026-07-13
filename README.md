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
│ run_all_scrapers.│      │  ┌──────────────────┐  │      │  Kartenansicht +  │
│  py              │      │  │     Scraper        │  │      │  Filterleiste     │
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

1. GitHub Actions triggert periodisch `backend/scripts/run_all_scrapers.py`.
2. Das Script startet Playwright und lässt jeden registrierten Scraper
   (`backend/app/scrapers/`) die Inserate-Seite seiner Genossenschaft
   parsen. Jeder Scraper implementiert dasselbe Interface
   (`BaseScraper.scrape(page) -> list[WohnungData]`), damit neue
   Genossenschaften ohne Änderungen am Rest des Systems ergänzt werden
   können. Schlägt ein Scraper fehl, wird der Fehler geloggt und die
   übrigen Scraper laufen trotzdem weiter; am Ende gibt das Script eine
   Zusammenfassung aus (neu/aktualisiert/fehlgeschlagen).
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
    models.py                  # SQLAlchemy-Modelle (Wohnung)
    crud.py                     # upsert_wohnung() inkl. Change-Detection per Hash
    schemas.py                  # Pydantic-Schemas für die API
    api/
      listings.py               # GET /listings mit Filtern
    scrapers/
      base.py                    # BaseScraper-Interface
      registry.py                 # Liste aller aktiven Scraper
      example_coop.py              # Vorlage für einen neuen Scraper
      abw_winterthur.py             # Scraper für die ABW Winterthur
    notifications/
      mailer.py                    # Mail-Versand bei neuen Inseraten
  scripts/
    run_all_scrapers.py           # Entrypoint für den Cron-Job
  alembic/
    env.py                        # liest DATABASE_URL aus app.config, kennt Base.metadata
    versions/                     # Migrationsskripte
  alembic.ini
  requirements.txt
  .env.example

frontend/
  src/
    App.jsx                      # Verdrahtet Filter + Karte + API
    components/
      MapView.jsx                 # Leaflet-Karte mit Markern
      FilterPanel.jsx              # Zimmer/Preis/Viertel-Filter
    api/
      client.js                    # fetch-Wrapper fürs Backend
  package.json

.github/workflows/
  scrape.yml                      # Cron-Trigger für run_all_scrapers.py
```

## Hosting (kostenlos)

- **Datenbank:** [Supabase](https://supabase.com) Free Tier (Postgres).
- **Scraper:** GitHub Actions Cron (im Free-Tier-Limit für private/öffentliche
  Repos ausreichend für einen Lauf alle 30 Minuten).
- **Backend:** [Render](https://render.com) Free Tier (Web Service via
  `render.yaml` im Repo-Root, `rootDir: backend`, Start-Command
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`). Benoetigte
  Env-Vars auf Render setzen: `DATABASE_URL`, `FRONTEND_ORIGIN`
  (die Vercel-Produktions-URL), `RESEND_API_KEY`, `MAIL_FROM`,
  `NOTIFY_EMAIL_TO`, `NOMINATIM_USER_AGENT`.
- **Frontend:** [Vercel](https://vercel.com) (Root-Verzeichnis des Projekts
  bleibt der Repo-Root, `vercel.json` baut `frontend/` und deployt
  `frontend/dist`). Env-Var `VITE_API_BASE_URL` auf die Render-Backend-URL
  setzen (z.B. `https://genossenschaft-backend.onrender.com`).

## Neuen Genossenschafts-Scraper hinzufügen

1. `backend/app/scrapers/<name>.py` anlegen, `BaseScraper` erben,
   `name`, `listing_url` und `scrape()` implementieren (gibt
   `list[WohnungData]` zurück).
2. Scraper in `backend/app/scrapers/registry.py` importieren und in
   `SCRAPERS` eintragen.

## Lokale Entwicklung (Grundgerüst)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # Werte anpassen, insb. DATABASE_URL
alembic upgrade head   # Schema in Supabase/Postgres anlegen
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
