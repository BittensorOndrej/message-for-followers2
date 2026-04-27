import logging
from typing import Optional
from .api import send_dm, reply_to_comment, has_existing_conversation
from .messages import MESSAGES

log = logging.getLogger(__name__)





def handle_new_follower(follower_id: str) -> None:
    log.info("👤 Nový follower: %s", follower_id)
    _send_if_no_conversation(follower_id)


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

