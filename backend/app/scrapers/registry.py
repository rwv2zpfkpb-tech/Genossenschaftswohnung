"""Zentrale Liste aller aktiven Scraper-Adapter.

Neuen Adapter hinzufuegen: Modul in adapters/ anlegen, ScraperAdapter
implementieren, hier importieren und in ADAPTERS eintragen.
"""
from app.scrapers.adapters.example_coop import ExampleCoopAdapter
from app.scrapers.base import ScraperAdapter

ADAPTERS: list[type[ScraperAdapter]] = [
    ExampleCoopAdapter,
]
