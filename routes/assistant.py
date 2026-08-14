"""API endpoint backing the floating AI Assistant widget (see base.html)."""

from flask import Blueprint, request, jsonify, session

from utils.decorators import login_required
from utils.ai_engine import get_assistant_reply

bp = Blueprint("assistant", __name__)


@bp.route("/api/assistant", methods=["POST"])
@login_required
def ask():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    page = (data.get("page") or "general").strip()
    context = data.get("context") or {}
    history = data.get("history") or []

    if not message:
        return jsonify({"reply": "Type a question and I'll help!"}), 400
    if len(message) > 1000:
        message = message[:1000]

    reply = get_assistant_reply(message, page=page, context=context, history=history)
    return jsonify({"reply": reply})
