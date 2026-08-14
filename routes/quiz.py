"""Aptitude Quiz: category selection, quiz taking, scoring."""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from models.db import get_db
from utils.decorators import login_required

bp = Blueprint("quiz", __name__)


@bp.route("/quiz")
@login_required
def categories():
    db = get_db()
    rows = db.execute(
        "SELECT category, COUNT(*) total FROM quiz_questions GROUP BY category"
    ).fetchall()
    return render_template("quiz.html", categories=rows)


@bp.route("/quiz/<category>", methods=["GET", "POST"])
@login_required
def take_quiz(category):
    db = get_db()
    difficulty = request.args.get("difficulty", "All")

    if request.method == "POST":
        questions_ids = request.form.getlist("question_id")
        score = 0
        wrong = []
        for qid in questions_ids:
            selected = request.form.get(f"answer_{qid}")
            row = db.execute(
                "SELECT * FROM quiz_questions WHERE id = ?", (qid,)
            ).fetchone()
            if row and selected == row["correct_option"]:
                score += 1
            elif row:
                wrong.append({"question": row["question"], "correct": row["correct_option"],
                              "selected": selected or "Not answered"})

        total = len(questions_ids)
        db.execute(
            "INSERT INTO quiz_results (user_id, category, score, total) VALUES (?, ?, ?, ?)",
            (session["user_id"], category, score, total),
        )
        db.commit()
        return render_template("quiz.html", result={"score": score, "total": total, "category": category},
                                wrong_answers=wrong,
                                categories=db.execute(
                                    "SELECT category, COUNT(*) total FROM quiz_questions GROUP BY category"
                                ).fetchall())

    if difficulty == "All":
        questions = db.execute(
            "SELECT * FROM quiz_questions WHERE category = ? ORDER BY RANDOM() LIMIT 10", (category,)
        ).fetchall()
    else:
        questions = db.execute(
            "SELECT * FROM quiz_questions WHERE category = ? AND difficulty = ? ORDER BY RANDOM() LIMIT 10",
            (category, difficulty),
        ).fetchall()

    if not questions:
        flash("No questions found for this category/difficulty yet.", "warning")
        return redirect(url_for("quiz.categories"))

    return render_template("quiz.html", questions=questions, category=category, categories=None,
                            active_difficulty=difficulty)
