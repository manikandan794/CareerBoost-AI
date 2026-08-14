"""Admin Dashboard: platform-wide stats, user & message management."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from models.db import get_db
from utils.decorators import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/admin")
@admin_required
def dashboard():
    db = get_db()

    stats = {
        "total_users": db.execute("SELECT COUNT(*) c FROM users WHERE is_admin = 0").fetchone()["c"],
        "total_resumes": db.execute("SELECT COUNT(*) c FROM resumes").fetchone()["c"],
        "total_quiz_attempts": db.execute("SELECT COUNT(*) c FROM quiz_results").fetchone()["c"],
        "unread_messages": db.execute("SELECT COUNT(*) c FROM contact_messages WHERE is_read = 0").fetchone()["c"],
        "total_ai_requests": db.execute("SELECT COUNT(*) c FROM ai_messages WHERE role = 'user'").fetchone()["c"],
        "total_gd_attempts": db.execute("SELECT COUNT(*) c FROM gd_sessions").fetchone()["c"],
        "total_ai_quiz_attempts": db.execute("SELECT COUNT(*) c FROM ai_quiz_attempts").fetchone()["c"],
        "total_roadmaps": db.execute("SELECT COUNT(*) c FROM career_roadmaps").fetchone()["c"],
    }

    avg_gd_row = db.execute("SELECT AVG(overall_score) avg_score FROM gd_evaluations").fetchone()
    stats["avg_gd_score"] = round(avg_gd_row["avg_score"], 1) if avg_gd_row["avg_score"] else 0

    avg_quiz_row = db.execute(
        "SELECT AVG((score * 1.0 / total) * 100) avg_pct FROM quiz_results"
    ).fetchone()
    stats["avg_quiz_score"] = round(avg_quiz_row["avg_pct"], 1) if avg_quiz_row["avg_pct"] else 0

    most_practiced_gd_topic = db.execute(
        "SELECT topic_title, COUNT(*) c FROM gd_sessions GROUP BY topic_title ORDER BY c DESC LIMIT 1"
    ).fetchone()
    stats["most_practiced_gd_topic"] = most_practiced_gd_topic["topic_title"] if most_practiced_gd_topic else "—"

    recent_users = db.execute(
        "SELECT * FROM users WHERE is_admin = 0 ORDER BY created_at DESC LIMIT 8"
    ).fetchall()

    recent_activity = db.execute(
        """SELECT 'Quiz' AS kind, u.full_name, qr.taken_at AS ts FROM quiz_results qr
           JOIN users u ON u.id = qr.user_id
           UNION ALL
           SELECT 'Group Discussion', u.full_name, gs.started_at FROM gd_sessions gs
           JOIN users u ON u.id = gs.user_id
           UNION ALL
           SELECT 'AI Roadmap', u.full_name, cr.created_at FROM career_roadmaps cr
           JOIN users u ON u.id = cr.user_id
           ORDER BY ts DESC LIMIT 10"""
    ).fetchall()

    messages = db.execute(
        "SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 8"
    ).fetchall()

    return render_template(
        "admin.html", stats=stats, recent_users=recent_users, messages=messages, recent_activity=recent_activity
    )


@bp.route("/admin/chart-data")
@admin_required
def chart_data():
    db = get_db()
    signups = db.execute(
        """SELECT DATE(created_at) d, COUNT(*) c FROM users
           WHERE is_admin = 0 GROUP BY DATE(created_at) ORDER BY d LIMIT 14"""
    ).fetchall()
    category_attempts = db.execute(
        "SELECT category, COUNT(*) c FROM quiz_results GROUP BY category"
    ).fetchall()

    return jsonify({
        "signup_labels": [r["d"] for r in signups],
        "signup_counts": [r["c"] for r in signups],
        "quiz_categories": [r["category"] for r in category_attempts],
        "quiz_counts": [r["c"] for r in category_attempts],
    })


@bp.route("/admin/users")
@admin_required
def users():
    db = get_db()
    all_users = db.execute(
        "SELECT * FROM users WHERE is_admin = 0 ORDER BY created_at DESC"
    ).fetchall()
    return render_template("admin_users.html", users=all_users)


@bp.route("/admin/messages/<int:msg_id>/read")
@admin_required
def mark_read(msg_id):
    db = get_db()
    db.execute("UPDATE contact_messages SET is_read = 1 WHERE id = ?", (msg_id,))
    db.commit()
    flash("Message marked as read.", "success")
    return redirect(url_for("admin.dashboard"))
