"""Versand von E-Mail-Benachrichtigungen bei neuen Inseraten."""
from app.config import get_settings
from app.models import Listing


def send_new_listing_notification(listings: list[Listing]) -> None:
    """Verschickt eine Mail mit allen neu gefundenen Inseraten.

    TODO: SMTP-Versand implementieren (z.B. ueber smtplib oder einen
    kostenlosen Transaktions-Mail-Dienst).
    """
    settings = get_settings()
    if not listings or not settings.notify_email_to:
        return
    raise NotImplementedError
