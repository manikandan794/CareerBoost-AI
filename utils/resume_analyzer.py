"""
A lightweight, dependency-free "ATS style" resume analyzer.

It does NOT call any external AI service — it scores resume text against
a target job description using keyword overlap, section detection and
basic formatting heuristics. This keeps the demo fully self-contained
while still giving genuinely useful, actionable feedback.
"""

import re

COMMON_SECTIONS = [
    "experience", "education", "skills", "projects",
    "summary", "certifications", "objective",
]

ACTION_VERBS = [
    "led", "built", "designed", "developed", "implemented", "created",
    "improved", "optimized", "managed", "achieved", "launched", "automated",
    "analyzed", "reduced", "increased", "collaborated",
]


def _tokenize(text: str):
    return set(re.findall(r"[a-zA-Z][a-zA-Z\+\#\.]{1,}", text.lower()))


def analyze_resume(resume_text: str, job_description: str = ""):
    resume_tokens = _tokenize(resume_text)
    result = {
        "word_count": len(resume_text.split()),
        "sections_found": [],
        "sections_missing": [],
        "action_verbs_used": [],
        "keyword_match_score": None,
        "matched_keywords": [],
        "missing_keywords": [],
        "overall_score": 0,
        "tips": [],
    }

    # ---- Section detection -----------------------------------------
    lower_text = resume_text.lower()
    for section in COMMON_SECTIONS:
        if section in lower_text:
            result["sections_found"].append(section.capitalize())
        else:
            result["sections_missing"].append(section.capitalize())

    # ---- Action verb usage -------------------------------------------
    result["action_verbs_used"] = sorted(
        [v for v in ACTION_VERBS if v in resume_tokens]
    )

    # ---- Keyword match against job description ------------------------
    score_components = []

    if job_description.strip():
        jd_tokens = _tokenize(job_description)
        jd_tokens = {t for t in jd_tokens if len(t) > 2}
        matched = jd_tokens & resume_tokens
        missing = jd_tokens - resume_tokens
        match_pct = round((len(matched) / len(jd_tokens)) * 100, 1) if jd_tokens else 0
        result["keyword_match_score"] = match_pct
        result["matched_keywords"] = sorted(matched)[:25]
        result["missing_keywords"] = sorted(missing)[:25]
        score_components.append(min(match_pct, 100))

    # ---- Section completeness score -----------------------------------
    section_score = (len(result["sections_found"]) / len(COMMON_SECTIONS)) * 100
    score_components.append(section_score)

    # ---- Action verb score ---------------------------------------------
    verb_score = min(len(result["action_verbs_used"]) * 12.5, 100)
    score_components.append(verb_score)

    # ---- Length score (sweet spot 300-800 words) ------------------------
    wc = result["word_count"]
    if 300 <= wc <= 800:
        length_score = 100
    elif wc < 300:
        length_score = max((wc / 300) * 100, 20)
    else:
        length_score = max(100 - (wc - 800) / 10, 30)
    score_components.append(length_score)

    result["overall_score"] = round(sum(score_components) / len(score_components))

    # ---- Tips ------------------------------------------------------------
    if result["sections_missing"]:
        result["tips"].append(
            f"Consider adding these sections: {', '.join(result['sections_missing'])}."
        )
    if len(result["action_verbs_used"]) < 5:
        result["tips"].append(
            "Use more strong action verbs (e.g. built, led, optimized) to describe achievements."
        )
    if wc < 300:
        result["tips"].append("Your resume looks short — add more detail on projects and impact.")
    elif wc > 800:
        result["tips"].append("Your resume is quite long — try to trim it to 1 page (~500-700 words).")
    if job_description.strip() and result["keyword_match_score"] is not None and result["keyword_match_score"] < 50:
        result["tips"].append(
            "Your resume matches less than half the job description's keywords — "
            "tailor your skills and experience section to the role."
        )
    if not result["tips"]:
        result["tips"].append("Great job! Your resume looks well-structured and complete.")

    return result
