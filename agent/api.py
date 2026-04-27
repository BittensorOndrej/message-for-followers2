import logging
import requests
from .config import Config

log = logging.getLogger(__name__)
_BASE = "https://graph.instagram.com/v21.0"


def has_existing_conversation(user_id: str) -> bool:
    """
    Zkontroluje přes Instagram API, zda už s uživatelem existuje konverzace.
    Vrátí True pokud spolu už píšete, False pokud ne.
    """
    url = f"{_BASE}/{Config.PAGE_ID}/conversations"
    params = {
        "platform":     "instagram",
        "user_id":      user_id,
        "access_token": Config.ACCESS_TOKEN,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        exists = len(data.get("data", [])) > 0
        log.info("🔍 Konverzace s %s: %s", user_id, "existuje" if exists else "neexistuje")
        return exists
    except requests.RequestException as exc:
        log.error("❌ Chyba při kontrole konverzace s %s: %s", user_id, exc)
        # Při chybě raději nepošleme zprávu (bezpečnější)
        return True


def send_dm(recipient_id: str, message: str) -> bool:
    """Odešle DM uživateli přes Instagram Messaging API."""
    url = f"{_BASE}/{Config.PAGE_ID}/messages"
    payload = {
        "recipient":    {"id": recipient_id},
        "message":      {"text": message},
        "access_token": Config.ACCESS_TOKEN,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        log.info("✅ DM odesláno → %s", recipient_id)
        return True
    except requests.RequestException as exc:
        log.error("❌ DM selhalo → %s: %s", recipient_id, exc)
        return False


def reply_to_comment(comment_id: str, message: str) -> bool:
    """Odpoví veřejně na komentář pod příspěvkem."""
    url = f"{_BASE}/{comment_id}/replies"
    payload = {
        "message":      message,
        "access_token": Config.ACCESS_TOKEN,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        log.info("✅ Odpověď na komentář %s odeslána", comment_id)
        return True
    except requests.RequestException as exc:
        log.error("❌ Odpověď selhala %s: %s", comment_id, exc)
        return False
