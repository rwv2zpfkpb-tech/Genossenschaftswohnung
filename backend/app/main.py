"""FastAPI-Einstiegspunkt."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import listings
from app.config import get_settings

settings = get_settings()

app = FastAPI(title="Genossenschaftswohnungen Zuerich API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_origin_regex=settings.frontend_origin_regex,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
