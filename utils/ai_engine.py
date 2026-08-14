"""
CareerBoost AI Assistant — a page-aware helper that guides students
through whatever section of the site they're currently using.

Two modes:

1. LLM-BACKED (primary, when configured): if a GEMINI_API_KEY
   environment variable is set, requests are answered by Gemini via
   utils.ai_tasks.assistant_reply(), which builds a system prompt
   describing the current page/context, giving fully dynamic,
   conversational answers.

2. RULE-BASED (automatic fallback, zero setup required): a hand-tuned
   knowledge engine that understands which page the learner is on
   (resume builder, coding practice, interview prep, aptitude quiz,
   ...) plus keywords in their message, and responds with concrete,
   actionable coaching. If the Gemini call fails for any reason (no
   key, network, quota, timeout) we transparently fall back to this
   mode so the assistant always responds — never a raw error.
"""

import re

PAGE_LABELS = {
    "resume-builder": "the Resume Builder",
    "resume-analyzer": "the Resume Analyzer",
    "coding-practice": "Coding Practice",
    "interview-questions": "Interview Questions",
    "quiz": "the Aptitude Quiz",
    "dashboard": "the Dashboard",
    "companies": "Company Insights",
    "ai-hub": "the AI Career Coach Hub",
    "ai-roadmap": "the AI Career Roadmap Generator",
    "ai-skill-gap": "the AI Skill Gap Analyzer",
    "ai-study": "the AI Study Assistant",
    "ai-quiz-generator": "the AI Quiz Generator",
    "ai-resume-match": "the AI Resume ↔ Job Description Matcher",
    "ai-company-prep": "AI Company Preparation",
    "ai-interview-coach": "the AI Mock Interview Coach",
    "group-discussion": "the Group Discussion Coach",
    "general": "CareerBoost AI",
}

LANGUAGE_LABELS = {
    "python": "Python",
    "javascript": "JavaScript",
    "c": "C",
    "cpp": "C++",
    "java": "Java",
    "html_css": "HTML/CSS",
}

# Common gotchas per language, surfaced when a learner says their tests are
# failing / their code won't run — this is what "more coding-language
# knowledge" mainly buys the rule-based (offline, no-API-key) mode.
_LANGUAGE_DEBUG_TIPS = {
    "python": "Common Python gotchas: mismatched indentation, using `=` instead of `==`, "
              "and forgetting to `return` a value (a function with no return implicitly returns None).",
    "javascript": "Common JavaScript gotchas: forgetting to `return` from arrow functions with `{ }` bodies, "
                  "comparing with `==` instead of `===`, and off-by-one errors with `.length`.",
    "c": "Common C gotchas: missing `&` before a variable in `scanf`, forgetting a `;`, array bounds "
         "(C won't stop you writing past the end), and not printing a trailing newline.",
    "cpp": "Common C++ gotchas: forgetting `using namespace std;` or `std::`, mismatched `cin >>` types, "
           "and off-by-one errors in loops over indices 0..n-1.",
    "java": "Common Java gotchas: the public class must be named exactly `Main`, `Scanner.nextInt()` "
            "leaves a trailing newline that can trip up a later `nextLine()`, and missing semicolons.",
    "html_css": "Common HTML/CSS gotchas: unclosed tags, a missing `;` after a CSS property, mixing up "
                "margin vs padding, and forgetting `display: flex` before using `justify-content`/`align-items`.",
}


# ======================================================================
#  MODE 1 — Gemini-backed reply (primary, when GEMINI_API_KEY is set)
# ======================================================================
def _try_llm_reply(message, page, context, history):
    from utils.gemini_service import is_configured
    if not is_configured():
        return None

    from utils import ai_tasks

    context = dict(context or {})
    if page == "coding-practice" and context.get("problem_language"):
        context["language_label"] = LANGUAGE_LABELS.get(context["problem_language"], context["problem_language"])

    result = ai_tasks.assistant_reply(message, PAGE_LABELS.get(page, page), context, history)
    return result.text if result.ok else None


# ======================================================================
#  MODE 1 — rule-based, page-aware engine
# ======================================================================
def _match(message, *keywords):
    m = message.lower()
    return any(k in m for k in keywords)


def _greeting_reply(page):
    return (
        f"Hey! I'm your CareerBoost AI Assistant. I can see you're on {PAGE_LABELS.get(page, 'this page')} — "
        "tell me what you're trying to do or where you're stuck and I'll help."
    )


def _resume_builder_reply(message, context):
    if _match(message, "summary", "objective"):
        return (
            "For your professional summary, use 2-3 lines: (1) who you are + your strongest skill area, "
            "(2) one quantified achievement or project, (3) what you're looking for. "
            "Example: \"Final-year CS student skilled in Python and SQL, built a 3-project portfolio including "
            "a full-stack booking app used by 50+ test users. Seeking an SDE internship where I can ship real features.\" "
            "Avoid generic lines like 'hardworking team player' — every sentence should carry a fact."
        )
    if _match(message, "skill", "skills"):
        return (
            "List 6-10 skills split by type (Languages, Frameworks, Tools) rather than one long comma list — "
            "recruiters and ATS parsers scan it faster. Only include skills you can defend in an interview, "
            "and mirror the exact wording used in the job description (e.g. write 'React.js' if that's what they wrote)."
        )
    if _match(message, "bullet", "experience", "describe", "internship", "project"):
        return (
            "Turn every bullet into: Action verb + what you built/did + measurable result. "
            "Weak: \"Worked on a website for the college fest.\" "
            "Strong: \"Built a fest registration website (Flask + SQLite) that processed 400+ signups and cut manual "
            "entry work by ~5 hours.\" Start each line with a strong verb — Built, Led, Automated, Reduced, Designed — "
            "and try to end with a number wherever you can."
        )
    if _match(message, "template", "design", "format", "look"):
        return (
            "Classic is the safest for ATS parsing and most core-company drives. Modern/Executive add a touch of "
            "colour and are fine for product companies and startups. Whatever you pick, keep it to one page, "
            "use one font, and avoid tables/columns that some ATS systems fail to parse correctly."
        )
    if _match(message, "ats", "keyword"):
        return (
            "To beat ATS keyword filters: paste the target job description into the Resume Analyzer tab, "
            "and add the exact technical keywords it lists (that you genuinely have) into your Skills and "
            "Experience sections — not just your summary, since some parsers weight repeated terms in context."
        )
    if _match(message, "length", "long", "short", "page"):
        return (
            "Aim for one page (roughly 400-650 words) if you have under ~3 years of experience. If a section "
            "is too short, add measurable detail to existing bullets rather than padding with filler sentences."
        )
    return (
        "I can help you write a stronger summary, tighten your experience/project bullets with real impact, "
        "pick the right skills to list, or explain ATS formatting. What part of the resume are you working on right now?"
    )


def _resume_analyzer_reply(message, context):
    if _match(message, "score", "low score", "why"):
        return (
            "Your score blends four things: how many resume sections are present, how many strong action verbs you "
            "used, whether your length is in the ~300-800 word sweet spot, and (if you pasted a job description) "
            "keyword overlap. Check the 'tips' list under your result — it tells you exactly which of those is "
            "pulling your score down."
        )
    if _match(message, "keyword", "missing"):
        return (
            "The 'missing keywords' list shows terms from the job description that don't appear anywhere in your "
            "resume text. Add the ones you genuinely have experience with into your Skills or Experience section — "
            "don't stuff in ones you can't speak to in an interview."
        )
    if _match(message, "action verb", "verb"):
        return (
            "Strong action verbs to weave in: Built, Designed, Implemented, Automated, Optimized, Led, Reduced, "
            "Increased, Launched, Analyzed, Migrated, Debugged. Replace passive phrasing like \"was responsible for\" "
            "with one of these at the start of the bullet."
        )
    return (
        "Paste your resume text and (optionally) a target job description into the analyzer, and I can help you "
        "interpret the score and prioritize which fix will move the needle most. What does your result currently show?"
    )


def _coding_reply(message, context):
    context = context or {}
    problem = context.get("problem_title")
    language = context.get("problem_language")
    lang_label = LANGUAGE_LABELS.get(language, language)
    prefix = f"On \"{problem}\"" + (f" ({lang_label})" if lang_label else "") + ": " if problem else ""

    if _match(message, "hint", "stuck", "don't know", "dont know", "help me", "idea"):
        if language == "html_css":
            return (
                prefix + "Try this: (1) get the HTML structure/nesting right first with no styling at all, "
                "(2) add layout (Flexbox/Grid) before visual polish, (3) style one element at a time and check "
                "the live preview after each change instead of writing all the CSS at once. Click 'Show a hint' "
                "on the left for a progressive nudge if you're still stuck."
            )
        return (
            prefix + "Try this before looking at a hint: (1) restate the problem in your own words, "
            "(2) work a tiny example by hand on paper, (3) name the data structure that example naturally "
            "suggests (a hash map for 'have I seen this before', a stack for 'nested/matching', two pointers "
            "for 'sorted array, looking for a pair'). Click 'Show a hint' on the left for a progressive nudge "
            "if you're still stuck after that."
        )
    if _match(message, "complexity", "big o", "time complexity", "space complexity"):
        return (
            "Think about it in two parts: how many times does your code touch each element (time), and how much "
            "extra memory scales with input size beyond the input itself (space). A single loop over n items is "
            "O(n); a loop inside a loop is usually O(n²) unless the inner loop shrinks meaningfully (like binary "
            "search, which is O(log n)). This reasoning is the same across Python, JS, C, C++ and Java — only "
            "the constant-factor speed differs, not the growth rate."
        )
    if _match(message, "compile", "compilation", "won't run", "wont run", "won't compile", "syntax error"):
        tip = _LANGUAGE_DEBUG_TIPS.get(language)
        return (
            (prefix + "Check the compiler error message shown above your results — it usually names the exact "
             "line. ") + (tip or "Read the error top to bottom; the first error is usually the real one, later "
                                  "ones are often just knock-on effects of it.")
        )
    if _match(message, "test", "fail", "wrong answer", "not passing"):
        tip = _LANGUAGE_DEBUG_TIPS.get(language)
        base = (
            "When a test fails, check the 'Expected' vs 'Got' values shown under that test case — often it's an "
            "off-by-one index, forgetting to handle an empty/edge-case input, or returning the wrong type/format. "
            "Try the exact failing input in your head or on paper step by step."
        )
        return prefix + base + (" " + tip if tip else "")
    if _match(message, "solution", "answer", "give me the code", "full code"):
        return (
            "I'll coach you toward the solution rather than hand it over — that's what actually sticks for "
            "interviews. Tell me which specific step you're blocked on (the approach, a bug, or the complexity) "
            "and I'll help you reason through just that part."
        )
    if language and _match(message, "language", "which language", "should i use", "switch language"):
        return (
            f"You're currently solving this in {lang_label} — Coding Practice also has Python, JavaScript, C, "
            "C++, Java and HTML/CSS problems if you want to practice a different one. Filter by language on the "
            "Coding Practice page to switch."
        )
    return (
        prefix + "I can help you pick an approach, debug a failing test/compile error, or reason about time/space "
        "complexity — what specifically are you stuck on?"
    )


def _interview_reply(message, context):
    if _match(message, "nervous", "anxious", "scared", "confidence"):
        return (
            "Totally normal. Two things help most: (1) prepare 3-4 stories in STAR format (Situation, Task, Action, "
            "Result) you can adapt to most behavioural questions, so you're never starting from a blank page, and "
            "(2) do at least one full mock run out loud, timed — the first time you hear your own voice answering "
            "should not be in the real interview."
        )
    if _match(message, "star", "star method"):
        return (
            "STAR = Situation (1 sentence of context), Task (what you specifically needed to do), Action (what "
            "you did — this should be the longest part), Result (the outcome, ideally with a number). Practice "
            "compressing it to under 90 seconds spoken aloud."
        )
    for topic in ("python", "dbms", "sql", "oop", "java", "operating system", "networks", "web development",
                  "cs fundamentals", "dsa"):
        if topic.replace(" ", "") in message.lower().replace(" ", ""):
            return (
                f"For {topic.title()} questions, don't just memorize definitions — for every concept, be ready to "
                "give one real example from something you've built, and know the follow-up 'why does this matter in "
                "practice' angle. Filter the question list on this page by that category and try answering out loud "
                "before revealing the model answer."
            )
    return (
        "I can help you structure an answer with the STAR method, calm pre-interview nerves, or point you to "
        "practice questions in a specific category (Python, DBMS, SQL, OOP, HR, etc). What would help right now?"
    )


def _quiz_reply(message, context):
    if _match(message, "quant", "math", "percentage", "profit", "interest", "time and work", "speed"):
        return (
            "Quantitative tip: memorize the core formulas (SI = PRT/100, profit% = (SP-CP)/CP × 100, work rate = "
            "1/days) so you're not deriving them under time pressure, and always sanity-check your final answer "
            "against the options — obviously-wrong-magnitude answers can be eliminated instantly."
        )
    if _match(message, "logic", "logical", "puzzle", "series", "coding-decoding", "blood relation"):
        return (
            "Logical reasoning tip: for coding-decoding, write out the alphabet with positions (A=1...Z=26) so "
            "shifts are visible; for blood-relation puzzles, sketch a quick family tree on paper rather than "
            "tracking it in your head; for number series, check differences, ratios, and squares/cubes in that order."
        )
    if _match(message, "verbal", "english", "grammar", "vocabulary", "synonym", "antonym"):
        return (
            "Verbal tip: read the full sentence before picking a fill-in-the-blank answer — tense and subject-verb "
            "agreement often eliminate 2 of 4 options immediately. For synonym/antonym questions, try the word in a "
            "short sentence of your own to feel out its connotation."
        )
    if _match(message, "technical", "cs", "programming"):
        return (
            "Technical MCQ tip: these test breadth over depth — know the *definitions and complexities* cold "
            "(sorting algorithms, data structure operations, SQL clauses, OOP pillars) since that's what's directly asked."
        )
    if _match(message, "wrong", "explain", "review"):
        return (
            "After finishing a quiz, check the 'Review — questions you missed' section on your result page — it "
            "shows your answer next to the correct one so you can see exactly where the reasoning went wrong."
        )
    return (
        "Ask me about strategy for a specific section — Quantitative, Logical, Verbal or Technical — or tell me "
        "which question type keeps tripping you up and I'll share a quick trick for it."
    )


def _general_reply(message):
    if _match(message, "hi", "hello", "hey", "sup"):
        return "Hey there! What are you working on — your resume, a coding problem, quiz prep, or interview practice?"
    if _match(message, "thank", "thanks", "thank you"):
        return "You're welcome! Good luck — come back anytime you get stuck."
    if _match(message, "what can you do", "help", "features"):
        return (
            "I can help across the whole platform: writing stronger resume bullets, explaining your resume analyzer "
            "score, giving coding-problem hints in Python, JavaScript, C, C++, Java or HTML/CSS (without spoiling "
            "the answer), coaching interview answers with the STAR method, and sharing quick strategy tips for "
            "each aptitude quiz category."
        )
    return (
        "I'm not totally sure what you mean — could you tell me a bit more, or say which part of the site "
        "(resume, coding, interview prep, or quiz) you need help with?"
    )


def rule_based_reply(message, page, context):
    if _match(message, "hi", "hello", "hey there", "sup") and len(message.strip()) < 12:
        return _greeting_reply(page)

    handlers = {
        "resume-builder": _resume_builder_reply,
        "resume-analyzer": _resume_analyzer_reply,
        "coding-practice": _coding_reply,
        "interview-questions": _interview_reply,
        "quiz": _quiz_reply,
    }
    handler = handlers.get(page)
    if handler:
        return handler(message, context)
    return _general_reply(message)


def get_assistant_reply(message, page="general", context=None, history=None):
    message = (message or "").strip()
    if not message:
        return "Go ahead and ask me something — I'm listening!"

    llm_reply = _try_llm_reply(message, page, context, history)
    if llm_reply:
        return llm_reply

    return rule_based_reply(message, page, context)
