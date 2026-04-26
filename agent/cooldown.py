import time
from .config import Config

_store: dict[str, float] = {}


def can_reply(user_id: str) -> bool:
    last = _store.get(user_id)
    return not (last and (time.time() - last) < Config.REPLY_COOLDOWN)


def mark_replied(user_id: str) -> None:
    _store[user_id] = time.time()
