"""Versand von E-Mail-Benachrichtigungen bei neuen Inseraten ueber Resend."""
from html import escape

import resend

from app.config import get_settings
from app.models import Wohnung

_PLACEHOLDER_IMAGE = "https://placehold.co/160x120?text=Kein+Bild"


def _format_preis(wohnung: Wohnung) -> str:
    return f"CHF {wohnung.preis}.-" if wohnung.preis is not None else "Preis auf Anfrage"


def _format_zimmer(wohnung: Wohnung) -> str:
    return f"{wohnung.zimmer} Zimmer" if wohnung.zimmer is not None else "Zimmerzahl unbekannt"


def _listing_row_html(wohnung: Wohnung) -> str:
    bild_url = wohnung.bild_urls[0] if wohnung.bild_urls else _PLACEHOLDER_IMAGE
    adresse = escape(wohnung.adresse)
    link = escape(wohnung.quelle_url)
    genossenschaft = escape(wohnung.genossenschaft)
    preis = escape(_format_preis(wohnung))
    zimmer = escape(_format_zimmer(wohnung))

    return f"""
    <tr>
      <td style="padding: 12px 0; border-bottom: 1px solid #e5e5e5;" valign="top">
        <a href="{link}">
          <img src="{escape(bild_url)}" width="120" height="90"
               alt="{adresse}"
               style="display:block; width:120px; height:90px; object-fit:cover; border-radius:6px; background:#f0f0f0;">
        </a>
      </td>
      <td style="padding: 12px 0 12px 16px; border-bottom: 1px solid #e5e5e5;" valign="top">
        <div style="font-size:16px; font-weight:600; margin-bottom:4px;">
          <a href="{link}" style="color:#1a1a1a; text-decoration:none;">{adresse}</a>
        </div>
        <div style="font-size:13px; color:#666; margin-bottom:6px;">{genossenschaft}</div>
        <div style="font-size:14px; color:#333;">{preis} &middot; {zimmer}</div>
        <div style="margin-top:6px;">
          <a href="{link}" style="font-size:13px; color:#2563eb;">Inserat ansehen &rarr;</a>
        </div>
      </td>
    </tr>
    """


def _build_html(listings: list[Wohnung]) -> str:
    rows_html = "".join(_listing_row_html(w) for w in listings)
    anzahl = len(listings)
    return f"""
    <html>
      <body style="font-family: -apple-system, Arial, sans-serif; background:#f7f7f7; padding:24px;">
        <table role="presentation" width="100%" style="max-width:600px; margin:0 auto; background:#fff; border-radius:8px; padding:24px;" cellpadding="0" cellspacing="0">
          <tr>
            <td>
              <h2 style="margin:0 0 16px; font-size:20px;">
                {anzahl} neue Genossenschaftswohnung(en) gefunden
              </h2>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                {rows_html}
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """


def send_new_listing_notification(listings: list[Wohnung]) -> None:
    """Verschickt eine Mail mit allen neu gefundenen Inseraten ueber Resend.

    Wird keine einzige neue Wohnung uebergeben, wird nichts verschickt.
    """
    settings = get_settings()
    if not listings or not settings.notify_email_to or not settings.resend_api_key:
        return

    resend.api_key = settings.resend_api_key
    resend.Emails.send(
        {
            "from": settings.mail_from,
            "to": [settings.notify_email_to],
            "subject": f"{len(listings)} neue Genossenschaftswohnung(en) gefunden",
            "html": _build_html(listings),
        }
    )
