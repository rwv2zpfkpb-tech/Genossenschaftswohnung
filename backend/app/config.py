"""Zentrale Konfiguration, aus Umgebungsvariablen geladen (.env)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Postgres / Supabase
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/genossenschaft"

    # Mail-Benachrichtigung (z.B. SMTP von einem kostenlosen Anbieter)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    notify_email_to: str = ""

    # CORS
    frontend_origin: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
