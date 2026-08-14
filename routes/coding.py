"""Coding Practice: browse problems across Python, JavaScript, C, C++, Java
and HTML/CSS, solve them in a real in-browser editor, and either run
automated test cases (Python/JS/C/C++/Java) or a live preview (HTML/CSS)."""

from flask import Blueprint, render_template, request, jsonify, abort

from models.db import get_db
from utils.decorators import login_required
from utils.code_runner import run_submission

bp = Blueprint("coding", __name__)

# Display metadata for each supported language.
LANGUAGES = {
    "python":     {"label": "Python",      "cm_mode": "python",        "icon": "bi-filetype-py"},
    "javascript": {"label": "JavaScript",  "cm_mode": "javascript",    "icon": "bi-filetype-js"},
    "c":          {"label": "C",           "cm_mode": "text/x-csrc",   "icon": "bi-filetype-c"},
    "cpp":        {"label": "C++",         "cm_mode": "text/x-c++src", "icon": "bi-filetype-cpp"},
    "java":       {"label": "Java",        "cm_mode": "text/x-java",   "icon": "bi-filetype-java"},
    "html_css":   {"label": "HTML / CSS",  "cm_mode": "htmlmixed",     "icon": "bi-filetype-html"},
}


@bp.route("/coding-practice")
@login_required
def index():
    db = get_db()
    difficulty = request.args.get("difficulty", "All")
    topic = request.args.get("topic", "All")
    language = request.args.get("language", "All")

    query = "SELECT * FROM coding_problems WHERE 1=1"
    params = []
    if difficulty != "All":
        query += " AND difficulty = ?"
        params.append(difficulty)
    if topic != "All":
        query += " AND topic = ?"
        params.append(topic)
    if language != "All":
        query += " AND language = ?"
        params.append(language)
    query += " ORDER BY id"

    problems = db.execute(query, params).fetchall()
    topics = [r["topic"] for r in db.execute(
        "SELECT DISTINCT topic FROM coding_problems ORDER BY topic"
    ).fetchall()]
    total_count = db.execute("SELECT COUNT(*) c FROM coding_problems").fetchone()["c"]

    return render_template(
        "coding.html", problems=problems, active_difficulty=difficulty,
        topics=topics, active_topic=topic, total_count=total_count,
        languages=LANGUAGES, active_language=language,
    )


@bp.route("/coding-practice/<int:problem_id>")
@login_required
def problem_detail(problem_id):
    db = get_db()
    problem = db.execute("SELECT * FROM coding_problems WHERE id = ?", (problem_id,)).fetchone()
    if not problem:
        abort(404)
    lang_info = LANGUAGES.get(problem["language"] or "python", LANGUAGES["python"])
    return render_template("coding_problem.html", p=problem, lang_info=lang_info)


@bp.route("/coding-practice/<int:problem_id>/run", methods=["POST"])
@login_required
def run_code(problem_id):
    db = get_db()
    problem = db.execute("SELECT * FROM coding_problems WHERE id = ?", (problem_id,)).fetchone()
    if not problem:
        return jsonify({"ok": False, "error": "Problem not found."}), 404

    if (problem["judge_type"] or "function") == "preview":
        return jsonify({"ok": False, "error": "This is an HTML/CSS layout problem — use the live "
                                               "preview panel instead of Run Tests."}), 400

    code = (request.json or {}).get("code", "")
    if not code.strip():
        return jsonify({"ok": False, "error": "Write some code before running it."}), 400

    if not problem["test_cases"] or (problem["judge_type"] == "function" and not problem["function_name"]):
        return jsonify({"ok": False, "error": "This problem doesn't have an automated judge yet."}), 400

    outcome = run_submission(code, problem)
    if outcome["ok"]:
        outcome["all_passed"] = all(r.get("passed") for r in outcome["results"]) if outcome["results"] else False
    return jsonify(outcome)
