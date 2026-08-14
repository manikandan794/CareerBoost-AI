"""User dashboard: progress overview + chart data endpoint."""

from flask import Blueprint, render_template, session, jsonify

from models.db import get_db
from utils.decorators import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
@login_required
def index():
    db = get_db()
    user_id = session["user_id"]

    quiz_results = db.execute(
        "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY taken_at DESC LIMIT 5",
        (user_id,),
    ).fetchall()

    total_quizzes = db.execute(
        "SELECT COUNT(*) c FROM quiz_results WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]

    avg_score_row = db.execute(
        "SELECT AVG( (score * 1.0 / total) * 100 ) avg_pct FROM quiz_results WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    avg_score = round(avg_score_row["avg_pct"], 1) if avg_score_row["avg_pct"] else 0

    resume_count = db.execute(
        "SELECT COUNT(*) c FROM resumes WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]

    return render_template(
        "dashboard.html",
        quiz_results=quiz_results,
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        resume_count=resume_count,
    )


@bp.route("/dashboard/chart-data")
@login_required
def chart_data():
    """JSON endpoint consumed by Chart.js on the dashboard page."""
    db = get_db()
    user_id = session["user_id"]

    rows = db.execute(
        """SELECT category, AVG((score * 1.0/total)*100) avg_pct, COUNT(*) attempts
           FROM quiz_results WHERE user_id = ? GROUP BY category""",
        (user_id,),
    ).fetchall()

    categories = [r["category"] for r in rows] or ["Quantitative", "Logical", "Verbal"]
    scores = [round(r["avg_pct"], 1) for r in rows] or [0, 0, 0]

    trend_rows = db.execute(
        """SELECT taken_at, (score*1.0/total)*100 pct FROM quiz_results
           WHERE user_id = ? ORDER BY taken_at ASC LIMIT 10""",
        (user_id,),
    ).fetchall()
    trend_labels = [r["taken_at"][:10] for r in trend_rows]
    trend_scores = [round(r["pct"], 1) for r in trend_rows]

    return jsonify({
        "categories": categories,
        "scores": scores,
        "trend_labels": trend_labels,
        "trend_scores": trend_scores,
    })
