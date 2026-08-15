"""
Gemini AI service layer for CareerBoost AI.

This is the ONE place in the codebase that talks to Google's Gemini
API. Every AI feature (Career Coach, Resume Coach, Interview Coach,
Coding Assistant, Study Assistant, Placement Coach, Group Discussion
simulator, AI Quiz Generator, ...) is built on top of the two
functions here — `generate()` and `generate_json()` — instead of each
route reimplementing HTTP calls and error handling.

Configuration
--------------
Set the GEMINI_API_KEY environment variable. NEVER hard-code it, put
it in a template, send it to the frontend, or log it.

    export GEMINI_API_KEY="your-key-here"        # macOS / Linux
    setx GEMINI_API_KEY "your-key-here"           # Windows

Get a free key at https://aistudio.google.com/app/apikey

Failure handling
-----------------
If the key is missing, invalid, rate-limited, times out, or the API
returns something unexpected, every public function here returns a
`GeminiResult` with `ok=False` and a short, user-friendly `.error`
message — it never raises. Callers show `.error` (or fall back to a
simpler rule-based response) instead of crashing or leaking a stack
trace to the user.
"""

import os
import re
import json
import logging

import requests

logger = logging.getLogger(__name__)

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_URL_TMPL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
REQUEST_TIMEOUT_SECONDS = 45

_SAFETY_SETTINGS = [
    {"category": c, "threshold": "BLOCK_ONLY_HIGH"}
    for c in (
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
    )
]


class GeminiResult:
    """Uniform return type for every Gemini call in the app."""

    def __init__(self, ok, text=None, data=None, error=None):
        self.ok = ok
        self.text = text      # raw text reply (for chat-style tasks)
        self.data = data      # parsed JSON (for generate_json)
        self.error = error    # user-friendly error message, only set when ok=False

    def __bool__(self):
        return self.ok

    def to_dict(self):
        if self.ok:
            return {"ok": True, "data": self.data, "text": self.text}
        return {"ok": False, "error": self.error}


def is_configured():
    """True if a GEMINI_API_KEY is present in the environment."""
    return bool(os.environ.get("GEMINI_API_KEY"))


def _post(payload):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return GeminiResult(
            False,
            error="AI features aren't configured yet — the platform admin needs to set a GEMINI_API_KEY.",
        )

    url = GEMINI_API_URL_TMPL.format(model=GEMINI_MODEL)
    try:
        resp = requests.post(url, params={"key": api_key}, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        return GeminiResult(False, error="The AI took too long to respond. Please try again.")
    except requests.exceptions.RequestException:
        logger.warning("Gemini request failed", exc_info=True)
        return GeminiResult(False, error="Couldn't reach the AI service right now. Please try again.")

    if resp.status_code in (401, 403):
        return GeminiResult(False, error="The configured GEMINI_API_KEY was rejected. Ask the admin to check it.")
    if resp.status_code == 429:
        return GeminiResult(False, error="The AI is getting a lot of requests right now (rate limit). Please wait a moment and try again.")
    if resp.status_code >= 500:
        return GeminiResult(False, error="Gemini is temporarily unavailable. Please try again shortly.")
    if resp.status_code != 200:
        logger.warning("Gemini returned status %s: %s", resp.status_code, resp.text[:500])
        return GeminiResult(False, error="The AI service returned an unexpected error. Please try again.")

    try:
        data = resp.json()
    except ValueError:
        return GeminiResult(False, error="The AI returned a response we couldn't read.")

    candidates = data.get("candidates") or []
    if not candidates:
        block_reason = (data.get("promptFeedback") or {}).get("blockReason")
        if block_reason:
            return GeminiResult(False, error="That request was blocked by the AI's safety filters. Try rephrasing it.")
        return GeminiResult(False, error="The AI didn't return a response. Please try again.")

    try:
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError, AttributeError, TypeError):
        return GeminiResult(False, error="Couldn't parse the AI's response.")

    finish_reason = candidates[0].get("finishReason")
    if not text:
        if finish_reason == "SAFETY":
            return GeminiResult(False, error="That request was blocked by the AI's safety filters. Try rephrasing it.")
        return GeminiResult(False, error="The AI returned an empty response. Please try again.")

    return GeminiResult(True, text=text)


def generate(system_instruction, user_prompt, history=None, temperature=0.7, max_tokens=1024):
    """
    Free-form conversational generation.

    history: optional list of {"role": "user"|"assistant", "content": str},
    most-recent-last. Only the last 8 turns are sent (keeps requests small
    and cheap, per the app's AI-usage-optimization requirement).
    """
    contents = []
    for turn in (history or [])[-8:]:
        role = "user" if turn.get("role") == "user" else "model"
        content = (turn.get("content") or "").strip()
        if content:
            contents.append({"role": role, "parts": [{"text": content}]})
    contents.append({"role": "user", "parts": [{"text": user_prompt}]})

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
        "safetySettings": _SAFETY_SETTINGS,
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    return _post(payload)


def _strip_code_fence(raw):
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE).strip()


def generate_json(system_instruction, user_prompt, temperature=0.5, max_tokens=2048):
    """
    Ask Gemini for structured JSON and parse it.

    Tolerates the model wrapping the JSON in markdown fences or a little
    prose around it (both happen in practice even with instructions not
    to). Returns GeminiResult with `.data` set to the parsed object/list
    on success, or `.error` set on failure — never raises.
    """
    strict_instruction = (
        (system_instruction or "").strip()
        + "\n\nRespond with ONLY valid JSON. No markdown code fences, no commentary, "
          "no leading or trailing text — the entire response must be parseable by json.loads()."
    )
    result = generate(strict_instruction, user_prompt, temperature=temperature, max_tokens=max_tokens)
    if not result.ok:
        return result

    raw = _strip_code_fence(result.text)
    try:
        result.data = json.loads(raw)
        return result
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\{.*\}|\[.*\])", raw, re.DOTALL)
    if match:
        try:
            result.data = json.loads(match.group(1))
            return result
        except json.JSONDecodeError:
            pass

    logger.warning("Gemini JSON parse failed. Raw (truncated): %s", raw[:800])
    return GeminiResult(False, error="The AI's response wasn't in the format we expected. Please try again.")
