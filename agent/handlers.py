from .api import send_dm, reply_to_comment, has_existing_conversation
import logging
from typing import Optional
from .api import send_dm, reply_to_comment, has_existing_conversation
from .messages import MESSAGES

log = logging.getLogger(__name__)


def _send_if_no_conversation(user_id: str) -> None:
    send_dm(user_id, MESSAGES["auto_reply"])



def handle_new_comment(
    commenter_id: str,
    comment_id: str,
    comment_text: str,
    post_id: Optional[str] = None,
) -> None:
    log.info("💬 Komentář od %s: %.60s", commenter_id, comment_text)
    _send_if_no_conversation(commenter_id)


def handle_incoming_dm(sender_id: str, text: str) -> None:
    log.info("📩 Příchozí DM od %s: %.80s", sender_id, text)
    
    # Klíčová slova která spustí automatickou odpověď
    KEYWORDS = ["flaer"]
    
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in KEYWORDS):
        log.info("🔑 Klíčové slovo nalezeno, odesílám odpověď")
        send_dm(sender_id, MESSAGES["auto_reply"])
