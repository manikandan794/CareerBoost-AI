"""Technical Interview Questions browser, grouped by category."""

from flask import Blueprint, render_template, request

from models.db import get_db
from utils.decorators import login_required

bp = Blueprint("interview", __name__)


@bp.route("/interview-questions")
@login_required
def index():
    db = get_db()
    category = request.args.get("category", "All")
    difficulty = request.args.get("difficulty", "All")

    categories = [r["category"] for r in db.execute(
        "SELECT DISTINCT category FROM interview_questions ORDER BY category"
    ).fetchall()]

    query = "SELECT * FROM interview_questions WHERE 1=1"
    params = []
    if category != "All":
        query += " AND category = ?"
        params.append(category)
    if difficulty != "All":
        query += " AND difficulty = ?"
        params.append(difficulty)
    query += " ORDER BY category, id"

    questions = db.execute(query, params).fetchall()
    total_count = db.execute("SELECT COUNT(*) c FROM interview_questions").fetchone()["c"]

    return render_template(
        "interview.html", questions=questions, categories=categories,
        active_category=category, active_difficulty=difficulty, total_count=total_count,
    )
