"""Zentrale Liste aller aktiven Scraper.

Neuen Scraper hinzufuegen: Modul in scrapers/ anlegen, BaseScraper
implementieren, hier importieren und in SCRAPERS eintragen.
"""
from app.scrapers.abw_winterthur import ABWWinterthurScraper
from app.scrapers.abz_zuerich import ABZZuerichScraper
from app.scrapers.alpenblick_horgen import AlpenblickHorgenScraper
from app.scrapers.base import BaseScraper
from app.scrapers.buchserstrasse_boppelsen import BuchserstrasseBoppelsenScraper
from app.scrapers.pwg_zuerich import PWGZuerichScraper

SCRAPERS: list[type[BaseScraper]] = [
    ABWWinterthurScraper,
    ABZZuerichScraper,
    AlpenblickHorgenScraper,
    BuchserstrasseBoppelsenScraper,
    PWGZuerichScraper,
]
