"""
AI Career Coach — task layer.

Each function here builds a purpose-specific prompt for one AI feature
and calls the low-level utils.gemini_service. Routes stay thin: they
validate input, call one of these, and render/return the result.

All functions return a utils.gemini_service.GeminiResult. Check
`.ok` before using `.data` / `.text`; on failure show `.error`.
"""

from utils.gemini_service import generate, generate_json

BASE_PERSONA = (
    "You are the CareerBoost AI Career Coach, embedded inside a student placement-preparation "
    "platform. You are encouraging but honest, concrete rather than generic, and you tailor advice "
    "to what the student actually tells you instead of giving one-size-fits-all answers. "
    "Never invent specific real-world facts (current hiring numbers, real company interview questions, "
    "real salary data) you cannot verify — if something needs current/real information you don't have, "
    "say the guidance is general rather than presenting it as verified fact."
)


# ---------------------------------------------------------------------------
# Context-aware general assistant (floating widget)
# ---------------------------------------------------------------------------
def assistant_reply(message, page_label, context, history):
    system = (
        BASE_PERSONA
        + f" The learner is currently on: {page_label}. Be warm, concise (under 130 words unless asked "
          "for more), and concrete. If they're on a coding problem, coach with hints and approaches — "
          "never dump a complete working solution unless they explicitly ask after already trying. "
          "If they're building a resume, give specific rewrites, not generic advice."
    )
    if context:
        system += f" Extra page context (JSON): {context}."
    return generate(system, message, history=history, temperature=0.7, max_tokens=500)


# ---------------------------------------------------------------------------
# Career Roadmap Generator
# ---------------------------------------------------------------------------
def career_roadmap(education_level, current_skills, target_role, experience_level, study_time, preferred_tech):
    system = (
        BASE_PERSONA
        + " Generate a personalized, realistic career roadmap for a student. "
          "Respond as JSON with EXACTLY this shape: "
          '{"career_goal": str, "required_skills": [str], "skill_gaps": [str], '
          '"weekly_plan": [{"week": str, "focus": str, "tasks": [str]}], '
          '"projects_to_build": [{"name": str, "description": str}], '
          '"practice_topics": [str], "interview_prep": [str], "resume_prep": [str], '
          '"placement_prep": [str], "milestones": [{"milestone": str, "target": str}]}. '
          "Keep weekly_plan to 6-10 weeks of realistic granularity (group into phases if longer). "
          "Keep every list item short (under 18 words)."
    )
    prompt = (
        f"Education level: {education_level}\n"
        f"Current skills: {current_skills}\n"
        f"Target job role: {target_role}\n"
        f"Experience level: {experience_level}\n"
        f"Available study time per week: {study_time}\n"
        f"Preferred technology/stack: {preferred_tech or 'no strong preference'}\n"
        "Build the roadmap now."
    )
    return generate_json(system, prompt, temperature=0.6, max_tokens=2500)


# ---------------------------------------------------------------------------
# Skill Gap Analyzer
# ---------------------------------------------------------------------------
def skill_gap_analysis(current_skills, target_role):
    system = (
        BASE_PERSONA
        + " Analyze a student's current skills against a target job role. Respond as JSON with EXACTLY "
          'this shape: {"existing_skills": [str], "missing_skills": [{"skill": str, "priority": '
          '"High"|"Medium"|"Low", "level": "Beginner"|"Intermediate"|"Advanced"}], '
          '"recommended_learning_order": [str], "practice_recommendations": [str], '
          '"project_recommendations": [str], "interview_topics": [str], "readiness_percent": int}. '
          "readiness_percent is 0-100, your honest estimate of how ready they are for that role today. "
          "Keep list items concise."
    )
    prompt = f"Current skills: {current_skills}\nTarget role: {target_role}\nAnalyze the gap now."
    return generate_json(system, prompt, temperature=0.5, max_tokens=1800)


# ---------------------------------------------------------------------------
# Study Assistant
# ---------------------------------------------------------------------------
STUDY_MODES = {
    "simple": "Give a simple, beginner-friendly explanation using an everyday analogy.",
    "detailed": "Give a detailed, thorough explanation covering the underlying mechanics.",
    "notes": "Write short, scannable revision notes using bullet points and bold key terms.",
    "exam_notes": "Write exam-focused notes: definitions, key formulas/points, and common trap areas.",
    "important_questions": "List the most likely exam/interview questions on this topic, each with a brief model answer.",
    "mcqs": "Generate 5 multiple-choice questions on this topic. For each: question, 4 options, correct option, 1-line explanation.",
    "flashcards": "Generate 8 flashcards on this topic as term/definition pairs, front and back.",
    "interview_questions": "List common interview questions on this topic with concise ideal-answer outlines.",
    "coding_examples": "Give 2-3 short, well-commented code examples that illustrate this topic in practice.",
    "real_world_examples": "Give 2-3 concrete real-world examples/use-cases of this topic.",
    "revision_plan": "Create a short day-by-day revision plan (3-5 days) to master this topic before an exam/interview.",
}


def study_material(topic, mode):
    mode_instruction = STUDY_MODES.get(mode, STUDY_MODES["simple"])
    system = (
        BASE_PERSONA
        + " You are the AI Study Assistant. Always respond with clean, structured Markdown "
          "(headings, bullet points, bold key terms) — never one huge unformatted paragraph. "
          f"Task: {mode_instruction}"
    )
    prompt = f"Topic: {topic}"
    return generate(system, prompt, temperature=0.6, max_tokens=1600)


# ---------------------------------------------------------------------------
# AI Quiz Generator
# ---------------------------------------------------------------------------
def generate_quiz(subject, topic, difficulty, num_questions):
    system = (
        BASE_PERSONA
        + " Generate an original multiple-choice quiz. Respond as a JSON array, each item EXACTLY: "
          '{"question": str, "option_a": str, "option_b": str, "option_c": str, "option_d": str, '
          '"correct_option": "A"|"B"|"C"|"D", "explanation": str}. '
          "Questions must be unambiguous with exactly one correct option. Do not repeat questions."
    )
    prompt = (
        f"Subject: {subject}\nTopic: {topic}\nDifficulty: {difficulty}\n"
        f"Number of questions: {num_questions}\nGenerate the quiz now."
    )
    return generate_json(system, prompt, temperature=0.7, max_tokens=2200)


def grade_quiz_weak_topics(subject, topic, missed_questions):
    """missed_questions: list of question strings the user got wrong."""
    if not missed_questions:
        return None
    system = (
        BASE_PERSONA
        + ' Respond as JSON: {"weak_topics": [str], "revision_tip": str}. '
          "weak_topics is 2-4 short sub-topic names inferred from which questions were missed."
    )
    prompt = (
        f"Subject: {subject}\nTopic: {topic}\nQuestions the student got WRONG:\n- "
        + "\n- ".join(missed_questions[:15])
    )
    return generate_json(system, prompt, temperature=0.4, max_tokens=400)


# ---------------------------------------------------------------------------
# Resume <-> Job Description matching
# ---------------------------------------------------------------------------
def resume_jd_match(resume_text, job_description):
    system = (
        BASE_PERSONA
        + " Compare a resume against a job description. Respond as JSON EXACTLY: "
          '{"match_score": int, "matching_skills": [str], "missing_skills": [str], '
          '"important_keywords": [str], "relevant_projects_feedback": str, '
          '"experience_alignment": str, "ats_suggestions": [str], "interview_prep_suggestions": [str]}. '
          "match_score is 0-100."
    )
    prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description}\n\nAnalyze the match now."
    return generate_json(system, prompt, temperature=0.4, max_tokens=1800)


# ---------------------------------------------------------------------------
# Company Preparation
# ---------------------------------------------------------------------------
def company_prep(company_name, target_role):
    system = (
        BASE_PERSONA
        + " Create a placement-preparation guide for a company/role. This must be labeled as GENERAL "
          "guidance, not verified current facts about the real company, since you cannot verify current "
          "hiring details. Respond as JSON EXACTLY: "
          '{"disclaimer": str, "company_overview": str, "expected_skills": [str], '
          '"technical_preparation": [str], "aptitude_preparation": [str], "coding_preparation": [str], '
          '"hr_preparation": [str], "frequently_expected_topics": [str], '
          '"mock_interview_plan": [str], "seven_day_strategy": [{"day": str, "focus": str}]}. '
          "The disclaimer field must clearly state this is general preparation guidance, not confirmed "
          "current information about the named company."
    )
    prompt = f"Company: {company_name}\nTarget role: {target_role or 'general fresher/entry-level role'}\nBuild the prep guide now."
    return generate_json(system, prompt, temperature=0.5, max_tokens=2000)


# ---------------------------------------------------------------------------
# AI Mock Interview Coach
# ---------------------------------------------------------------------------
def interview_first_question(category, mode):
    system = (
        BASE_PERSONA
        + f" You are running a {mode} mock interview in the category '{category}'. "
          "Ask exactly ONE realistic interview question, nothing else — no preamble, no numbering."
    )
    return generate(system, "Ask the first question.", temperature=0.8, max_tokens=120)


def interview_feedback_and_next(category, mode, question, answer, question_number):
    system = (
        BASE_PERSONA
        + f" You are running a {mode} mock interview in the category '{category}'. The student just "
          "answered a question. Respond as JSON EXACTLY: "
          '{"score": int, "strengths": [str], "weaknesses": [str], "improvement_tip": str, '
          '"next_question": str}. score is 0-10. next_question must be ONE new, different interview '
          f"question in the same category (this will be question #{question_number + 1})."
    )
    prompt = f"Question asked: {question}\nStudent's answer: {answer}\nEvaluate and give the next question."
    return generate_json(system, prompt, temperature=0.6, max_tokens=700)


def interview_final_report(category, mode, transcript):
    system = (
        BASE_PERSONA
        + f" The mock {mode} interview ({category}) has ended. Respond as JSON EXACTLY: "
          '{"overall_score": int, "summary": str, "strengths": [str], "weaknesses": [str], '
          '"improvement_plan": [str], "confidence_tip": str}. overall_score is 0-100.'
    )
    transcript_text = "\n".join(f"{t['role']}: {t['content']}" for t in transcript)
    return generate_json(system, transcript_text, temperature=0.5, max_tokens=1200)


# ---------------------------------------------------------------------------
# Coding assistant helpers (used by the context-aware widget, and reusable
# for a dedicated "explain/debug/improve" action from the coding page)
# ---------------------------------------------------------------------------
def coding_assist(action, language, problem_title, code, error_message, question):
    action_instructions = {
        "explain": "Explain what this code does, step by step, in plain language.",
        "debug": "Find the bug(s) in this code. Explain what's wrong and how to fix it — give a corrected snippet only for the broken part, not a full rewrite unless necessary.",
        "improve": "Suggest concrete improvements (readability, efficiency, edge cases). Don't just say 'looks good'.",
        "explain_error": "Explain this error message in plain language and what likely causes it in this code.",
        "hint": "Give a progressive hint toward solving this — do NOT reveal the full solution.",
    }
    instruction = action_instructions.get(action, action_instructions["hint"])
    system = (
        BASE_PERSONA
        + f" You are the AI Coding Assistant. Language: {language or 'unspecified'}. "
          f"Problem: {problem_title or 'general practice'}. Task: {instruction} "
          "Keep the response focused and under 220 words unless a code block is required."
    )
    prompt_parts = []
    if code:
        prompt_parts.append(f"Student's code:\n```{language or ''}\n{code}\n```")
    if error_message:
        prompt_parts.append(f"Error message:\n{error_message}")
    if question:
        prompt_parts.append(f"Student's question: {question}")
    prompt = "\n\n".join(prompt_parts) or "No code provided yet — give general guidance for this problem."
    return generate(system, prompt, temperature=0.5, max_tokens=700)


# ---------------------------------------------------------------------------
# Group Discussion simulator
# ---------------------------------------------------------------------------
def gd_ai_turn(topic, difficulty, participant_names, transcript, round_number):
    """
    Ask Gemini to play 1-2 AI participants for the next turn of a GD.
    Returns JSON: {"turns": [{"speaker": str, "message": str}, ...]}
    """
    names_list = ", ".join(participant_names)
    system = (
        BASE_PERSONA
        + " You are simulating a realistic Group Discussion with multiple AI participants for placement "
          f"practice. Topic: \"{topic}\" (difficulty: {difficulty}). AI participants in this discussion: "
          f"{names_list}. A real student ('You') is also participating. "
          "AI participants must NOT all agree with each other — give genuinely different viewpoints, "
          "respectful disagreement, and build on or challenge points 'You' or other participants made. "
          "Keep each participant's turn to 2-4 sentences, natural spoken-discussion tone (not essay-like). "
          'Respond as JSON EXACTLY: {"turns": [{"speaker": str, "message": str}]}. '
          "Produce 1 or 2 turns from DIFFERENT AI participants (never from 'You'), continuing the discussion naturally."
        )
    transcript_text = "\n".join(f"{m['speaker']}: {m['message']}" for m in transcript[-14:]) or "(discussion has not started yet)"
    prompt = f"Discussion so far (round {round_number}):\n{transcript_text}\n\nGenerate the next turn(s)."
    return generate_json(system, prompt, temperature=0.85, max_tokens=500)


def gd_coaching_tip(topic, transcript):
    system = (
        BASE_PERSONA
        + " Give ONE short, specific coaching tip (under 20 words) to help the student speak better in "
          "this ongoing Group Discussion — e.g. suggesting an example, connecting to the topic, or "
          "responding to another participant. Do not write their answer for them."
    )
    transcript_text = "\n".join(f"{m['speaker']}: {m['message']}" for m in transcript[-10:])
    prompt = f"Topic: {topic}\nDiscussion so far:\n{transcript_text}\n\nGive one coaching tip."
    return generate(system, prompt, temperature=0.7, max_tokens=60)


def gd_evaluate(topic, difficulty, transcript):
    system = (
        BASE_PERSONA
        + " The Group Discussion has ended. Evaluate ONLY the messages from speaker 'You'. "
          "Respond as JSON EXACTLY: "
          '{"overall_score": int, "communication_score": int, "relevance_score": int, "clarity_score": int, '
          '"confidence_score": int, "topic_knowledge_score": int, "logical_thinking_score": int, '
          '"listening_score": int, "leadership_score": int, "team_participation_score": int, '
          '"vocabulary_score": int, "structure_score": int, "strong_points": [str], "weak_points": [str], '
          '"mistakes": [str], "better_alternatives": [str], "improvement_plan": [str]}. '
          "All *_score fields are 0-100. Be honest and specific, not generic."
    )
    transcript_text = "\n".join(f"{m['speaker']}: {m['message']}" for m in transcript)
    prompt = f"Topic: {topic} (difficulty: {difficulty})\n\nFull transcript:\n{transcript_text}\n\nEvaluate 'You' now."
    return generate_json(system, prompt, temperature=0.4, max_tokens=1800)
