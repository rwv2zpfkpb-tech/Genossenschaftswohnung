"""Manueller Test fuer das Notification-Modul mit Testdaten (ohne Scraper-Lauf).

Baut ein paar Beispiel-Wohnungen und schickt sie durch
send_new_listing_notification. So laesst sich das Mail-Layout und der
Resend-Versand isoliert pruefen, ohne einen echten Scraper laufen zu lassen.

Aufruf:
    python -m scripts.test_mailer            # verschickt eine echte Testmail
                                              # (benoetigt RESEND_API_KEY und
                                              # NOTIFY_EMAIL_TO in .env)
    python -m scripts.test_mailer --dry-run   # schreibt das HTML stattdessen
                                               # in eine Datei zum Ansehen im
                                               # Browser, kein Versand
"""
import argparse
import webbrowser
from pathlib import Path

from app.models import Wohnung
from app.notifications.mailer import _build_html, send_new_listing_notification

_TESTDATEN = [
    Wohnung(
        genossenschaft="ABZ",
        quelle_url="https://www.abz.ch/wohnungen/beispiel-1",
        adresse="Musterstrasse 12, 8003 Zuerich",
        viertel="Wiedikon",
        zimmer=3.5,
        preis=1850,
        beschreibung="Helle 3.5-Zimmer-Wohnung mit Balkon.",
        bild_urls=["https://picsum.photos/seed/wohnung1/400/300"],
    ),
    Wohnung(
        genossenschaft="Familienheim Zuerich",
        quelle_url="https://www.familienheim-zuerich.ch/wohnungen/beispiel-2",
        adresse="Beispielweg 4, 8004 Zuerich",
        viertel="Aussersihl",
        zimmer=2.0,
        preis=None,
        beschreibung="2-Zimmer-Wohnung, Preis auf Anfrage.",
        bild_urls=[],
    ),
    Wohnung(
        genossenschaft="ABW Winterthur",
        quelle_url="https://www.abwwin.ch/wohnungen/beispiel-3",
        adresse="Teststrasse 7, 8400 Winterthur",
        viertel=None,
        zimmer=None,
        preis=2200,
        beschreibung="4.5-Zimmer-Maisonette.",
        bild_urls=["https://picsum.photos/seed/wohnung3/400/300"],
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Kein Versand ueber Resend, stattdessen HTML in eine Datei schreiben und im Browser oeffnen.",
    )
    args = parser.parse_args()

    if args.dry_run:
        html = _build_html(_TESTDATEN)
        out_path = Path(__file__).resolve().parent.parent / "test_mailer_preview.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"Vorschau geschrieben nach {out_path}")
        webbrowser.open(out_path.as_uri())
        return

    send_new_listing_notification(_TESTDATEN)
    print(
        "Testmail verschickt (falls RESEND_API_KEY und NOTIFY_EMAIL_TO in .env gesetzt sind)."
    )


if __name__ == "__main__":
    main()
