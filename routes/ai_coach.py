"""
AI Career Coach — the multi-task AI hub (Career Roadmap, Skill Gap
Analyzer, Study Assistant, AI Quiz Generator, Resume<->JD Matcher,
Company Preparation, AI Mock Interview Coach).

Pattern used on every tool below:
  GET  /ai/<tool>          -> render the tool's page (form + empty result area)
  POST /api/ai/<tool>      -> JSON API the page's JS calls; runs the Gemini
                               task via utils.ai_tasks, saves a history row
                               where relevant, and returns JSON.

Keeping the Gemini calls behind JSON endpoints (rather than full-page
POSTs) keeps every tool page fast and lets the frontend show proper
loading/error states without a full reload.
"""

import json

from flask import Blueprint, render_template, request, jsonify, session

from models.db import get_db
from utils.decorators import login_required
from utils.gemini_service import is_configured
from utils import ai_tasks

bp = Blueprint("ai_coach", __name__)


# ======================================================================
#  Hub
# ======================================================================
@bp.route("/ai")
@login_required
def hub():
    db = get_db()
    user_id = session["user_id"]
    recent_roadmap = db.execute(
        "SELECT * FROM career_roadmaps WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,)
    ).fetchone()
    recent_skill_gap = db.execute(
        "SELECT * FROM skill_gap_reports WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,)
    ).fetchone()
    return render_template(
        "ai_hub.html",
        gemini_configured=is_configured(),
        recent_roadmap=recent_roadmap,
        recent_skill_gap=recent_skill_gap,
    )


# ======================================================================
#  Career Roadmap Generator
# ======================================================================
@bp.route("/ai/roadmap")
@login_required
def roadmap_page():
    db = get_db()
    history = db.execute(
        "SELECT * FROM career_roadmaps WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
        (session["user_id"],),
    ).fetchall()
    return render_template("ai_roadmap.html", gemini_configured=is_configured(), history=history)


@bp.route("/api/ai/roadmap", methods=["POST"])
@login_required
def api_roadmap():
    data = request.get_json(silent=True) or {}
    education_level = (data.get("education_level") or "").strip()
    current_skills = (data.get("current_skills") or "").strip()
    target_role = (data.get("target_role") or "").strip()
    experience_level = (data.get("experience_level") or "Beginner").strip()
    study_time = (data.get("study_time") or "").strip()
    preferred_tech = (data.get("preferred_tech") or "").strip()

    if not target_role:
        return jsonify({"ok": False, "error": "Please enter a target job role."}), 400

    result = ai_tasks.career_roadmap(
        education_level, current_skills, target_role, experience_level, study_time, preferred_tech
    )
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    db = get_db()
    db.execute(
        """INSERT INTO career_roadmaps
           (user_id, target_role, education_level, current_skills, experience_level, study_time,
            preferred_tech, roadmap_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session["user_id"], target_role, education_level, current_skills, experience_level,
            study_time, preferred_tech, json.dumps(result.data),
        ),
    )
    db.commit()
    return jsonify({"ok": True, "roadmap": result.data})


# ======================================================================
#  Skill Gap Analyzer
# ======================================================================
@bp.route("/ai/skill-gap")
@login_required
def skill_gap_page():
    db = get_db()
    history = db.execute(
        "SELECT * FROM skill_gap_reports WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
        (session["user_id"],),
    ).fetchall()
    return render_template("ai_skill_gap.html", gemini_configured=is_configured(), history=history)


@bp.route("/api/ai/skill-gap", methods=["POST"])
@login_required
def api_skill_gap():
    data = request.get_json(silent=True) or {}
    current_skills = (data.get("current_skills") or "").strip()
    target_role = (data.get("target_role") or "").strip()

    if not current_skills or not target_role:
        return jsonify({"ok": False, "error": "Please fill in both your current skills and the target role."}), 400

    result = ai_tasks.skill_gap_analysis(current_skills, target_role)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    db = get_db()
    db.execute(
        """INSERT INTO skill_gap_reports (user_id, target_role, current_skills, report_json, readiness_percent)
           VALUES (?, ?, ?, ?, ?)""",
        (session["user_id"], target_role, current_skills, json.dumps(result.data), result.data.get("readiness_percent")),
    )
    db.commit()
    return jsonify({"ok": True, "report": result.data})


# ======================================================================
#  Study Assistant
# ======================================================================
@bp.route("/ai/study")
@login_required
def study_page():
    return render_template("ai_study.html", gemini_configured=is_configured(), modes=list(ai_tasks.STUDY_MODES.keys()))


@bp.route("/api/ai/study", methods=["POST"])
@login_required
def api_study():
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or "").strip()
    mode = (data.get("mode") or "simple").strip()

    if not topic:
        return jsonify({"ok": False, "error": "Please enter a topic."}), 400
    if mode not in ai_tasks.STUDY_MODES:
        mode = "simple"

    result = ai_tasks.study_material(topic, mode)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    return jsonify({"ok": True, "content": result.text})


# ======================================================================
#  AI Quiz Generator
# ======================================================================
@bp.route("/ai/quiz-generator")
@login_required
def quiz_generator_page():
    db = get_db()
    history = db.execute(
        "SELECT * FROM ai_quiz_attempts WHERE user_id = ? ORDER BY taken_at DESC LIMIT 8",
        (session["user_id"],),
    ).fetchall()
    return render_template("ai_quiz_generator.html", gemini_configured=is_configured(), history=history)


@bp.route("/api/ai/quiz-generate", methods=["POST"])
@login_required
def api_quiz_generate():
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    topic = (data.get("topic") or "").strip()
    difficulty = (data.get("difficulty") or "Medium").strip()
    try:
        num_questions = max(3, min(int(data.get("num_questions") or 5), 15))
    except (TypeError, ValueError):
        num_questions = 5

    if not subject or not topic:
        return jsonify({"ok": False, "error": "Please enter both a subject and a topic."}), 400

    result = ai_tasks.generate_quiz(subject, topic, difficulty, num_questions)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    if not isinstance(result.data, list) or not result.data:
        return jsonify({"ok": False, "error": "The AI didn't return usable questions. Please try again."}), 502

    return jsonify({
        "ok": True,
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "questions": result.data,
    })


@bp.route("/api/ai/quiz-submit", methods=["POST"])
@login_required
def api_quiz_submit():
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    topic = (data.get("topic") or "").strip()
    difficulty = (data.get("difficulty") or "Medium").strip()
    questions = data.get("questions") or []
    answers = data.get("answers") or {}

    if not questions:
        return jsonify({"ok": False, "error": "No quiz to submit."}), 400

    score = 0
    missed = []
    for i, q in enumerate(questions):
        given = answers.get(str(i))
        correct = q.get("correct_option")
        if given and correct and given.upper() == correct.upper():
            score += 1
        else:
            missed.append(q.get("question", ""))

    weak_result = ai_tasks.grade_quiz_weak_topics(subject, topic, missed) if missed else None
    weak_topics = None
    revision_tip = None
    if weak_result and weak_result.ok:
        weak_topics = weak_result.data.get("weak_topics")
        revision_tip = weak_result.data.get("revision_tip")

    db = get_db()
    db.execute(
        """INSERT INTO ai_quiz_attempts (user_id, subject, topic, difficulty, questions_json, score, total, weak_topics)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session["user_id"], subject, topic, difficulty, json.dumps(questions),
            score, len(questions), json.dumps(weak_topics) if weak_topics else None,
        ),
    )
    db.commit()

    return jsonify({
        "ok": True,
        "score": score,
        "total": len(questions),
        "weak_topics": weak_topics,
        "revision_tip": revision_tip,
    })


# ======================================================================
#  Resume <-> Job Description Matching
# ======================================================================
@bp.route("/ai/resume-match")
@login_required
def resume_match_page():
    return render_template("ai_resume_match.html", gemini_configured=is_configured())


@bp.route("/api/ai/resume-match", methods=["POST"])
@login_required
def api_resume_match():
    data = request.get_json(silent=True) or {}
    resume_text = (data.get("resume_text") or "").strip()
    job_description = (data.get("job_description") or "").strip()

    if not resume_text or not job_description:
        return jsonify({"ok": False, "error": "Please provide both your resume text and the job description."}), 400

    result = ai_tasks.resume_jd_match(resume_text[:6000], job_description[:4000])
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    return jsonify({"ok": True, "match": result.data})


# ======================================================================
#  Company Preparation
# ======================================================================
@bp.route("/ai/company-prep")
@login_required
def company_prep_page():
    db = get_db()
    companies = db.execute("SELECT id, name FROM companies ORDER BY name").fetchall()
    return render_template("ai_company_prep.html", gemini_configured=is_configured(), companies=companies)


@bp.route("/api/ai/company-prep", methods=["POST"])
@login_required
def api_company_prep():
    data = request.get_json(silent=True) or {}
    company_name = (data.get("company_name") or "").strip()
    target_role = (data.get("target_role") or "").strip()

    if not company_name:
        return jsonify({"ok": False, "error": "Please enter a company name."}), 400

    result = ai_tasks.company_prep(company_name, target_role)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    return jsonify({"ok": True, "prep": result.data})


# ======================================================================
#  AI Mock Interview Coach
# ======================================================================
@bp.route("/ai/interview-coach")
@login_required
def interview_coach_page():
    return render_template("ai_interview_coach.html", gemini_configured=is_configured())


@bp.route("/api/ai/interview/start", methods=["POST"])
@login_required
def api_interview_start():
    data = request.get_json(silent=True) or {}
    category = (data.get("category") or "General").strip()
    mode = (data.get("mode") or "Technical").strip()

    result = ai_tasks.interview_first_question(category, mode)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    db = get_db()
    cur = db.execute(
        "INSERT INTO ai_conversations (user_id, tool, meta) VALUES (?, 'interview_coach', ?)",
        (session["user_id"], json.dumps({"category": category, "mode": mode, "question_number": 1})),
    )
    conversation_id = cur.lastrowid
    db.execute(
        "INSERT INTO ai_messages (conversation_id, role, content) VALUES (?, 'assistant', ?)",
        (conversation_id, result.text),
    )
    db.commit()

    return jsonify({"ok": True, "conversation_id": conversation_id, "question": result.text, "question_number": 1})


@bp.route("/api/ai/interview/answer", methods=["POST"])
@login_required
def api_interview_answer():
    data = request.get_json(silent=True) or {}
    conversation_id = data.get("conversation_id")
    answer = (data.get("answer") or "").strip()

    if not conversation_id or not answer:
        return jsonify({"ok": False, "error": "Missing conversation or answer."}), 400

    db = get_db()
    convo = db.execute(
        "SELECT * FROM ai_conversations WHERE id = ? AND user_id = ? AND tool = 'interview_coach'",
        (conversation_id, session["user_id"]),
    ).fetchone()
    if not convo:
        return jsonify({"ok": False, "error": "Interview session not found."}), 404

    meta = json.loads(convo["meta"] or "{}")
    category, mode = meta.get("category", "General"), meta.get("mode", "Technical")
    question_number = meta.get("question_number", 1)

    last_q = db.execute(
        "SELECT content FROM ai_messages WHERE conversation_id = ? AND role = 'assistant' ORDER BY id DESC LIMIT 1",
        (conversation_id,),
    ).fetchone()
    question_text = last_q["content"] if last_q else ""

    db.execute(
        "INSERT INTO ai_messages (conversation_id, role, content) VALUES (?, 'user', ?)",
        (conversation_id, answer),
    )

    result = ai_tasks.interview_feedback_and_next(category, mode, question_text, answer, question_number)
    if not result.ok:
        db.commit()
        return jsonify({"ok": False, "error": result.error}), 502

    fb = result.data
    db.execute(
        "INSERT INTO ai_messages (conversation_id, role, content, meta) VALUES (?, 'assistant', ?, ?)",
        (conversation_id, fb.get("next_question", ""), json.dumps({"feedback_for_question": question_number})),
    )
    new_question_number = question_number + 1
    db.execute(
        "UPDATE ai_conversations SET meta = ? WHERE id = ?",
        (json.dumps({"category": category, "mode": mode, "question_number": new_question_number}), conversation_id),
    )
    db.commit()

    return jsonify({
        "ok": True,
        "score": fb.get("score"),
        "strengths": fb.get("strengths"),
        "weaknesses": fb.get("weaknesses"),
        "improvement_tip": fb.get("improvement_tip"),
        "next_question": fb.get("next_question"),
        "question_number": new_question_number,
    })


@bp.route("/api/ai/interview/report", methods=["POST"])
@login_required
def api_interview_report():
    data = request.get_json(silent=True) or {}
    conversation_id = data.get("conversation_id")

    db = get_db()
    convo = db.execute(
        "SELECT * FROM ai_conversations WHERE id = ? AND user_id = ? AND tool = 'interview_coach'",
        (conversation_id, session["user_id"]),
    ).fetchone()
    if not convo:
        return jsonify({"ok": False, "error": "Interview session not found."}), 404

    meta = json.loads(convo["meta"] or "{}")
    category, mode = meta.get("category", "General"), meta.get("mode", "Technical")

    messages = db.execute(
        "SELECT role, content FROM ai_messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,),
    ).fetchall()
    transcript = [{"role": m["role"], "content": m["content"]} for m in messages]

    if len(transcript) < 2:
        return jsonify({"ok": False, "error": "Answer at least one question before requesting a report."}), 400

    result = ai_tasks.interview_final_report(category, mode, transcript)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502

    db.execute("UPDATE ai_conversations SET status = 'completed' WHERE id = ?", (conversation_id,))
    db.commit()

    return jsonify({"ok": True, "report": result.data})


# ======================================================================
#  Coding Assistant (used by an "Ask AI" action on the coding problem page)
# ======================================================================
@bp.route("/api/ai/coding-assist", methods=["POST"])
@login_required
def api_coding_assist():
    data = request.get_json(silent=True) or {}
    action = (data.get("action") or "hint").strip()
    language = (data.get("language") or "").strip()
    problem_title = (data.get("problem_title") or "").strip()
    code = (data.get("code") or "")[:4000]
    error_message = (data.get("error_message") or "")[:1000]
    question = (data.get("question") or "").strip()

    result = ai_tasks.coding_assist(action, language, problem_title, code, error_message, question)
    if not result.ok:
        return jsonify({"ok": False, "error": result.error}), 502
    return jsonify({"ok": True, "reply": result.text})
