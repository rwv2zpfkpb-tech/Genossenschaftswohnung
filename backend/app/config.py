"""Zentrale Konfiguration, aus Umgebungsvariablen geladen (.env)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Postgres / Supabase
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/genossenschaft"

    # Mail-Benachrichtigung ueber Resend (https://resend.com)
    resend_api_key: str = ""
    mail_from: str = "onboarding@resend.dev"
    notify_email_to: str = ""

    # CORS. frontend_origin ist die feste Produktions-URL, frontend_origin_regex
    # deckt zusaetzlich Vercel-Preview-Deployments ab (deren Subdomain sich pro
    # Deploy aendert).
    frontend_origin: str = "http://localhost:5173"
    frontend_origin_regex: str = r"https://.*\.vercel\.app"

    # Geocoding via Nominatim (https://nominatim.org) - Nutzungsbedingungen
    # verlangen einen identifizierenden User-Agent, idealerweise mit Kontakt.
    nominatim_user_agent: str = "genossenschaft-wohnungssuche/1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
