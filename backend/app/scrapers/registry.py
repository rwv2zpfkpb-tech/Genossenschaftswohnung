"""Zentrale Liste aller aktiven Scraper.

Neuen Scraper hinzufuegen: Modul in scrapers/ anlegen, BaseScraper
implementieren, hier importieren und in SCRAPERS eintragen.
"""
from app.scrapers.abw_winterthur import ABWWinterthurScraper
from app.scrapers.abz_zuerich import ABZZuerichScraper
from app.scrapers.base import BaseScraper

SCRAPERS: list[type[BaseScraper]] = [
    ABWWinterthurScraper,
    ABZZuerichScraper,
]
