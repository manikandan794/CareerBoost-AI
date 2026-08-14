"""
Group Discussion module — a Gemini-simulated multi-participant GD
practice environment with scoring and performance history.

Flow:
  GET  /gd                       -> dashboard (stats, categories, recent)
  GET  /gd/topics                -> browse topics by category
  POST /gd/start                 -> create a session, redirect to it
  GET  /gd/session/<id>          -> live simulation page
  POST /api/gd/<id>/message      -> user speaks; AI participants reply (JSON)
  POST /api/gd/<id>/tip          -> optional AI coaching tip (JSON)
  POST /api/gd/<id>/end          -> end + evaluate (JSON)
  GET  /gd/result/<id>           -> evaluation result page
  GET  /gd/history               -> performance history + progression
"""

import json
import random

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session

from models.db import get_db
from utils.decorators import login_required
from utils.gemini_service import is_configured
from utils import ai_tasks

bp = Blueprint("gd", __name__)

PARTICIPANT_NAMES = ["Participant A", "Participant B", "Participant C", "Participant D"]


def _participants_for(count):
    return PARTICIPANT_NAMES[: max(1, min(count, len(PARTICIPANT_NAMES)))]


# ======================================================================
#  Dashboard
# ======================================================================
@bp.route("/gd")
@login_required
def home():
    db = get_db()
    user_id = session["user_id"]

    attempts = db.execute(
        """SELECT s.id, s.topic_title, s.difficulty, s.started_at, e.overall_score,
                  e.communication_score, e.confidence_score, e.topic_knowledge_score
           FROM gd_sessions s LEFT JOIN gd_evaluations e ON e.session_id = s.id
           WHERE s.user_id = ? AND s.status = 'completed'
           ORDER BY s.started_at DESC LIMIT 5""",
        (user_id,),
    ).fetchall()

    stats_row = db.execute(
        """SELECT COUNT(*) attempts, AVG(e.overall_score) avg_overall,
                  AVG(e.communication_score) avg_comm, AVG(e.confidence_score) avg_conf
           FROM gd_sessions s JOIN gd_evaluations e ON e.session_id = s.id
           WHERE s.user_id = ?""",
        (user_id,),
    ).fetchone()

    categories = db.execute(
        "SELECT category, COUNT(*) c FROM gd_topics GROUP BY category ORDER BY category"
    ).fetchall()

    return render_template(
        "gd_home.html",
        gemini_configured=is_configured(),
        attempts=attempts,
        stats=stats_row,
        categories=categories,
    )


# ======================================================================
#  Topics
# ======================================================================
@bp.route("/gd/topics")
@login_required
def topics():
    db = get_db()
    category = request.args.get("category", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    query = "SELECT * FROM gd_topics WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    query += " ORDER BY category, title"

    topic_rows = db.execute(query, params).fetchall()
    all_categories = [r["category"] for r in db.execute("SELECT DISTINCT category FROM gd_topics ORDER BY category").fetchall()]

    return render_template(
        "gd_topics.html",
        topics=topic_rows,
        all_categories=all_categories,
        selected_category=category,
        selected_difficulty=difficulty,
    )


# ======================================================================
#  Start / run a session
# ======================================================================
@bp.route("/gd/start", methods=["POST"])
@login_required
def start():
    db = get_db()
    topic_id = request.form.get("topic_id", type=int)
    custom_topic = (request.form.get("custom_topic") or "").strip()
    difficulty = request.form.get("difficulty", "Medium")
    participant_count = max(1, min(request.form.get("participant_count", 3, type=int) or 3, 4))
    time_limit = request.form.get("time_limit", 10, type=int) or 10

    topic_title = custom_topic
    if topic_id and not topic_title:
        topic_row = db.execute("SELECT title, difficulty FROM gd_topics WHERE id = ?", (topic_id,)).fetchone()
        if topic_row:
            topic_title = topic_row["title"]
            difficulty = topic_row["difficulty"]

    if not topic_title:
        flash("Please choose or enter a discussion topic.", "warning")
        return redirect(url_for("gd.topics"))

    cur = db.execute(
        """INSERT INTO gd_sessions (user_id, topic_id, topic_title, difficulty, participant_count, time_limit_minutes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session["user_id"], topic_id, topic_title, difficulty, participant_count, time_limit),
    )
    db.commit()
    return redirect(url_for("gd.session_page", session_id=cur.lastrowid))


@bp.route("/gd/session/<int:session_id>")
@login_required
def session_page(session_id):
    db = get_db()
    gd_session = db.execute(
        "SELECT * FROM gd_sessions WHERE id = ? AND user_id = ?", (session_id, session["user_id"])
    ).fetchone()
    if not gd_session:
        flash("That discussion session was not found.", "warning")
        return redirect(url_for("gd.home"))

    if gd_session["status"] == "completed":
        return redirect(url_for("gd.result", session_id=session_id))

    messages = db.execute(
        "SELECT speaker, message FROM gd_messages WHERE session_id = ? ORDER BY id ASC", (session_id,)
    ).fetchall()

    return render_template(
        "gd_session.html",
        gd_session=gd_session,
        messages=messages,
        participants=_participants_for(gd_session["participant_count"]),
        gemini_configured=is_configured(),
    )


def _load_transcript(db, session_id):
    rows = db.execute(
        "SELECT speaker, message FROM gd_messages WHERE session_id = ? ORDER BY id ASC", (session_id,)
    ).fetchall()
    return [{"speaker": r["speaker"], "message": r["message"]} for r in rows]


@bp.route("/api/gd/<int:session_id>/message", methods=["POST"])
@login_required
def api_message(session_id):
    db = get_db()
    gd_session = db.execute(
        "SELECT * FROM gd_sessions WHERE id = ? AND user_id = ? AND status = 'active'",
        (session_id, session["user_id"]),
    ).fetchone()
    if not gd_session:
        return jsonify({"ok": False, "error": "Session not found or already ended."}), 404

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"ok": False, "error": "Say something to the group first."}), 400

    db.execute(
        "INSERT INTO gd_messages (session_id, speaker, message) VALUES (?, 'You', ?)",
        (session_id, message),
    )
    db.commit()

    participants = _participants_for(gd_session["participant_count"])
    transcript = _load_transcript(db, session_id)
    round_number = sum(1 for m in transcript if m["speaker"] == "You")

    result = ai_tasks.gd_ai_turn(gd_session["topic_title"], gd_session["difficulty"], participants, transcript, round_number)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    turns = result.data.get("turns") if isinstance(result.data, dict) else None
    if not turns:
        return jsonify({"ok": False, "error": "The AI participants didn't respond. Please try again."}), 502

    saved_turns = []
    for t in turns[:2]:
        speaker = t.get("speaker") or random.choice(participants)
        if speaker not in participants:
            speaker = random.choice(participants)
        text = (t.get("message") or "").strip()
        if not text:
            continue
        db.execute(
            "INSERT INTO gd_messages (session_id, speaker, message) VALUES (?, ?, ?)",
            (session_id, speaker, text),
        )
        saved_turns.append({"speaker": speaker, "message": text})
    db.commit()

    return jsonify({"ok": True, "turns": saved_turns})


@bp.route("/api/gd/<int:session_id>/tip", methods=["POST"])
@login_required
def api_tip(session_id):
    db = get_db()
    gd_session = db.execute(
        "SELECT * FROM gd_sessions WHERE id = ? AND user_id = ? AND status = 'active'",
        (session_id, session["user_id"]),
    ).fetchone()
    if not gd_session:
        return jsonify({"ok": False, "error": "Session not found or already ended."}), 404

    transcript = _load_transcript(db, session_id)
    if not transcript:
        return jsonify({"ok": False, "error": "Say something first so there's context for a tip."}), 400

    result = ai_tasks.gd_coaching_tip(gd_session["topic_title"], transcript)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    return jsonify({"ok": True, "tip": result.text})


@bp.route("/api/gd/<int:session_id>/end", methods=["POST"])
@login_required
def api_end(session_id):
    db = get_db()
    gd_session = db.execute(
        "SELECT * FROM gd_sessions WHERE id = ? AND user_id = ?", (session_id, session["user_id"])
    ).fetchone()
    if not gd_session:
        return jsonify({"ok": False, "error": "Session not found."}), 404

    if gd_session["status"] == "completed":
        return jsonify({"ok": True, "redirect": url_for("gd.result", session_id=session_id)})

    transcript = _load_transcript(db, session_id)
    if not any(m["speaker"] == "You" for m in transcript):
        return jsonify({"ok": False, "error": "Say at least one thing in the discussion before ending it."}), 400

    result = ai_tasks.gd_evaluate(gd_session["topic_title"], gd_session["difficulty"], transcript)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    ev = result.data
    db.execute(
        """INSERT INTO gd_evaluations
           (session_id, user_id, overall_score, communication_score, relevance_score, clarity_score,
            confidence_score, topic_knowledge_score, logical_thinking_score, listening_score,
            leadership_score, team_participation_score, vocabulary_score, structure_score,
            strong_points, weak_points, mistakes, better_alternatives, improvement_plan)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id, session["user_id"],
            ev.get("overall_score"), ev.get("communication_score"), ev.get("relevance_score"),
            ev.get("clarity_score"), ev.get("confidence_score"), ev.get("topic_knowledge_score"),
            ev.get("logical_thinking_score"), ev.get("listening_score"), ev.get("leadership_score"),
            ev.get("team_participation_score"), ev.get("vocabulary_score"), ev.get("structure_score"),
            json.dumps(ev.get("strong_points") or []), json.dumps(ev.get("weak_points") or []),
            json.dumps(ev.get("mistakes") or []), json.dumps(ev.get("better_alternatives") or []),
            json.dumps(ev.get("improvement_plan") or []),
        ),
    )
    db.execute(
        "UPDATE gd_sessions SET status = 'completed', ended_at = CURRENT_TIMESTAMP WHERE id = ?",
        (session_id,),
    )
    db.commit()

    return jsonify({"ok": True, "redirect": url_for("gd.result", session_id=session_id)})


@bp.route("/gd/result/<int:session_id>")
@login_required
def result(session_id):
    db = get_db()
    gd_session = db.execute(
        "SELECT * FROM gd_sessions WHERE id = ? AND user_id = ?", (session_id, session["user_id"])
    ).fetchone()
    if not gd_session:
        flash("That discussion session was not found.", "warning")
        return redirect(url_for("gd.home"))

    evaluation = db.execute("SELECT * FROM gd_evaluations WHERE session_id = ?", (session_id,)).fetchone()
    if not evaluation:
        flash("This session hasn't been evaluated yet.", "info")
        return redirect(url_for("gd.session_page", session_id=session_id))

    messages = db.execute(
        "SELECT speaker, message FROM gd_messages WHERE session_id = ? ORDER BY id ASC", (session_id,)
    ).fetchall()

    ev = dict(evaluation)
    for field in ("strong_points", "weak_points", "mistakes", "better_alternatives", "improvement_plan"):
        try:
            ev[field] = json.loads(ev[field]) if ev[field] else []
        except (TypeError, json.JSONDecodeError):
            ev[field] = []

    return render_template("gd_result.html", gd_session=gd_session, ev=ev, messages=messages)


# ======================================================================
#  History
# ======================================================================
@bp.route("/gd/history")
@login_required
def history():
    db = get_db()
    user_id = session["user_id"]

    rows = db.execute(
        """SELECT s.id, s.topic_title, s.difficulty, s.started_at, e.*
           FROM gd_sessions s JOIN gd_evaluations e ON e.session_id = s.id
           WHERE s.user_id = ? ORDER BY s.started_at ASC""",
        (user_id,),
    ).fetchall()

    if rows:
        avg_of = lambda key: round(sum((r[key] or 0) for r in rows) / len(rows), 1)
        category_avgs = {
            "Communication": avg_of("communication_score"),
            "Relevance": avg_of("relevance_score"),
            "Clarity": avg_of("clarity_score"),
            "Confidence": avg_of("confidence_score"),
            "Topic Knowledge": avg_of("topic_knowledge_score"),
            "Logical Thinking": avg_of("logical_thinking_score"),
            "Leadership": avg_of("leadership_score"),
        }
        strongest = max(category_avgs, key=category_avgs.get)
        weakest = min(category_avgs, key=category_avgs.get)
    else:
        category_avgs, strongest, weakest = {}, None, None

    recommended = db.execute(
        "SELECT title, category FROM gd_topics ORDER BY RANDOM() LIMIT 3"
    ).fetchall()

    return render_template(
        "gd_history.html",
        attempts=list(reversed(rows)),
        chart_labels=[r["started_at"][:10] for r in rows],
        chart_scores=[r["overall_score"] for r in rows],
        category_avgs=category_avgs,
        strongest=strongest,
        weakest=weakest,
        recommended=recommended,
    )
