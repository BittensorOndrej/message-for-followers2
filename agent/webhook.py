import hmac
import hashlib
import json
import logging
from flask import Flask, request, jsonify
from .config import Config
from .handlers import handle_new_follower, handle_new_comment, handle_incoming_dm

log = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/webhook", methods=["GET"])
    def webhook_verify():
        mode      = request.args.get("hub.mode")
        token     = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == Config.VERIFY_TOKEN:
            log.info("✅ Webhook ověřen.")
            return challenge, 200
        log.warning("❌ Webhook ověření selhalo.")
        return "Forbidden", 403

    @app.route("/webhook", methods=["POST"])
    def webhook_receive():
        sig = request.headers.get("X-Hub-Signature-256", "")
        if not _verify_signature(request.data, sig):
            log.warning("❌ Neplatný podpis.")
            return "Unauthorized", 401

        data = request.get_json(silent=True) or {}
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                _dispatch(change)
        return jsonify({"status": "ok"}), 200

    @app.route("/", methods=["GET"])
    def health():
        return jsonify({"status": "running"}), 200

    return app


def _verify_signature(payload: bytes, signature: str) -> bool:
    if not Config.APP_SECRET:
        log.warning("APP_SECRET není nastaven!")
        return True
    expected = "sha256=" + hmac.new(
        Config.APP_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def _dispatch(change: dict) -> None:
    field = change.get("field")
    value = change.get("value", {})

    if field == "follow":
        follower_id = value.get("sender_id") or value.get("id")
        if follower_id:
            handle_new_follower(str(follower_id))

    elif field == "comments":
        commenter_id = value.get("from", {}).get("id") or value.get("sender_id")
        comment_id   = value.get("id")
        comment_text = value.get("text", "")
        post_id      = value.get("media", {}).get("id")
        if commenter_id and comment_id:
            handle_new_comment(str(commenter_id), str(comment_id), comment_text, post_id)

    elif field == "messages":
        sender_id = value.get("sender", {}).get("id")
        text      = value.get("message", {}).get("text", "")
        if sender_id:
            handle_incoming_dm(str(sender_id), text)
