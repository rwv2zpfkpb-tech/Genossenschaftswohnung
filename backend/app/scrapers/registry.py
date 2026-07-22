"""Zentrale Liste aller aktiven Scraper.

Neuen Scraper hinzufuegen: Modul in scrapers/ anlegen, BaseScraper
implementieren, hier importieren und in SCRAPERS eintragen.
"""
from app.scrapers.abw_winterthur import ABWWinterthurScraper
from app.scrapers.abz_zuerich import ABZZuerichScraper
from app.scrapers.alpenblick_horgen import AlpenblickHorgenScraper
from app.scrapers.aurora_esslingen import AuroraEsslingenScraper
from app.scrapers.bachtel_hinwil import BachtelHinwilScraper
from app.scrapers.base import BaseScraper
from app.scrapers.bep_zuerich import BEPZuerichScraper
from app.scrapers.bg_duebendorf import BGDuebendorfScraper
from app.scrapers.bon_lieu import BonLieuScraper
from app.scrapers.bsh_zuerich import BSHZuerichScraper
from app.scrapers.bsz_schoenau import BSZSchoenauScraper
from app.scrapers.buchserstrasse_boppelsen import BuchserstrasseBoppelsenScraper
from app.scrapers.buwo_bubikon import BUWOBubikonScraper
from app.scrapers.ga_duernten import GADuerntenScraper
from app.scrapers.gbb_zuerich import GBBZuerichScraper
from app.scrapers.gbl_zuerich import GBLZuerichScraper
from app.scrapers.pwg_zuerich import PWGZuerichScraper
from app.scrapers.saw_zuerich import SAWZuerichScraper

SCRAPERS: list[type[BaseScraper]] = [
    ABWWinterthurScraper,
    ABZZuerichScraper,
    AlpenblickHorgenScraper,
    AuroraEsslingenScraper,
    BachtelHinwilScraper,
    BEPZuerichScraper,
    BGDuebendorfScraper,
    BonLieuScraper,
    BSHZuerichScraper,
    BSZSchoenauScraper,
    BuchserstrasseBoppelsenScraper,
    BUWOBubikonScraper,
    GADuerntenScraper,
    GBBZuerichScraper,
    GBLZuerichScraper,
    PWGZuerichScraper,
    SAWZuerichScraper,
]
