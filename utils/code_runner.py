"""
Multi-language code judge for the Coding Practice section.

Supports three judging strategies, dispatched by a problem's
`judge_type` + `language`:

  "function"  (python, javascript) — the learner implements a single
              function; the judge calls it directly with each test
              case's arguments and compares the return value.

  "stdio"     (c, cpp, java)       — the learner writes a full program
              that reads from stdin and writes to stdout; the judge
              compiles it once and runs it once per test case,
              comparing trimmed stdout to the expected text.

  "preview"   (html_css)           — not auto-graded; the frontend
              renders the learner's markup in a live iframe instead
              (see routes/coding.py — run_code() rejects these before
              ever reaching this module).

This is intentionally simple — a small, self-contained judge for a
student practice tool running on a single trusted host. It is NOT a
hardened, multi-tenant production sandbox (no containers/seccomp/
cgroups), so it should not be exposed to untrusted internet traffic
without further isolation.

Language runtimes required on the host for each judge to work:
  python    -> the same interpreter running Flask (always available)
  javascript-> `node` on PATH
  c         -> `gcc` on PATH
  cpp       -> `g++` on PATH
  java      -> `javac` + `java` on PATH
If a runtime isn't installed, that language's judge fails with a
clear "not installed" message instead of crashing the request.
"""

import json
import subprocess
import sys
import tempfile
import os
import textwrap
from typing import Optional

TIMEOUT_SECONDS = 5       # per test-case execution
COMPILE_TIMEOUT_SECONDS = 15

# ----------------------------------------------------------------------
# Conservative denylists: block the most obviously dangerous escape
# hatches (filesystem, network, process control) per language while
# staying out of the way of normal exercise code.
# ----------------------------------------------------------------------
BLOCKED_TOKENS = {
    "python": [
        "import os", "import sys", "import subprocess", "import shutil",
        "import socket", "import requests", "import urllib", "import ctypes",
        "import multiprocessing", "import threading", "__import__",
        "open(", "eval(", "exec(", "compile(", "globals(", "locals(",
        "__builtins__", "__class__", "__bases__", "__subclasses__",
    ],
    "javascript": [
        "require(", "import(", "process.", "child_process", "fs.", "net.",
        "eval(", "Function(", "__proto__", "constructor.constructor",
    ],
    "c": ["system(", "popen(", "fork(", "execl", "execv", "remove(", "unlink("],
    "cpp": ["system(", "popen(", "fork(", "execl", "execv", "remove(", "unlink(", "std::system"],
    "java": ["Runtime.getRuntime", "ProcessBuilder", "System.exit", "java.io.File", "java.nio.file"],
}


def _contains_blocked_token(code: str, language: str) -> Optional[str]:
    lowered = code.lower()
    for token in BLOCKED_TOKENS.get(language, []):
        if token.lower() in lowered:
            return token
    return None


def _blocked_response(token: str):
    return {
        "ok": False,
        "error": f"For safety, this judge doesn't allow using '{token.strip()}'. "
                 f"Solve the problem with plain language features and standard I/O only.",
        "results": [],
    }


# ======================================================================
#  Public entry point
# ======================================================================
def run_submission(code: str, problem) -> dict:
    """
    Run `code` against `problem`'s stored test cases, dispatching on
    problem['language'] / problem['judge_type'].

    Returns a dict: {"ok": bool, "error": str|None, "results": [...]}
    """
    language = (problem["language"] or "python").lower()
    judge_type = (problem["judge_type"] or "function").lower()
    test_cases_json = problem["test_cases"]
    function_name = problem["function_name"]

    blocked = _contains_blocked_token(code, language)
    if blocked:
        return _blocked_response(blocked)

    if judge_type == "function":
        if language == "python":
            return _run_python_function(code, function_name, test_cases_json)
        if language == "javascript":
            return _run_javascript_function(code, function_name, test_cases_json)
        return {"ok": False, "error": f"No function-style judge available for '{language}'.", "results": []}

    if judge_type == "stdio":
        if language in ("c", "cpp", "java"):
            return _run_stdio(language, code, test_cases_json)
        return {"ok": False, "error": f"No stdio judge available for '{language}'.", "results": []}

    return {"ok": False, "error": "This problem uses the live preview instead of automated tests.", "results": []}


# ======================================================================
#  PYTHON — function judge (subprocess, its own interpreter)
# ======================================================================
_PY_RUNNER_TEMPLATE = """
import json, sys

{user_code}

_test_cases = json.loads({test_cases_json!r})
_results = []
for _args, _expected in _test_cases:
    try:
        _actual = {function_name}(*_args)
        _passed = _actual == _expected
        _results.append({{"passed": _passed, "expected": _expected, "actual": _actual}})
    except Exception as _e:
        _results.append({{"passed": False, "expected": _expected, "actual": None, "error": str(_e)}})

print("__CB_RESULT_START__")
print(json.dumps(_results))
print("__CB_RESULT_END__")
"""


def _run_python_function(code: str, function_name: str, test_cases_json: str):
    try:
        test_cases = json.loads(test_cases_json)
    except (TypeError, ValueError):
        test_cases = []

    script = _PY_RUNNER_TEMPLATE.format(
        user_code=textwrap.indent(code, ""),
        test_cases_json=json.dumps(test_cases),
        function_name=function_name,
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        tmp_path = f.name

    try:
        proc = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Your code timed out (exceeded {TIMEOUT_SECONDS}s). "
                                       f"Check for infinite loops.", "results": []}
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    return _parse_marker_output(proc)


# ======================================================================
#  JAVASCRIPT — function judge (subprocess via `node`)
# ======================================================================
_JS_RUNNER_TEMPLATE = """
{user_code}

const _testCases = {test_cases_json};
const _results = [];
for (const [_args, _expected] of _testCases) {{
  try {{
    const _actual = {function_name}(..._args);
    const _passed = JSON.stringify(_actual) === JSON.stringify(_expected);
    _results.push({{ passed: _passed, expected: _expected, actual: _actual }});
  }} catch (_e) {{
    _results.push({{ passed: false, expected: _expected, actual: null, error: String(_e && _e.message || _e) }});
  }}
}}
console.log("__CB_RESULT_START__");
console.log(JSON.stringify(_results));
console.log("__CB_RESULT_END__");
"""


def _run_javascript_function(code: str, function_name: str, test_cases_json: str):
    try:
        test_cases = json.loads(test_cases_json)
    except (TypeError, ValueError):
        test_cases = []

    script = _JS_RUNNER_TEMPLATE.format(
        user_code=code,
        test_cases_json=json.dumps(test_cases),
        function_name=function_name,
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(script)
        tmp_path = f.name

    try:
        proc = subprocess.run(
            ["node", tmp_path],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return {"ok": False, "error": "JavaScript isn't available on this server (Node.js is not installed). "
                                       "Ask an admin to install Node.js to enable this judge.", "results": []}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Your code timed out (exceeded {TIMEOUT_SECONDS}s). "
                                       f"Check for infinite loops.", "results": []}
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    return _parse_marker_output(proc)


def _parse_marker_output(proc):
    """Shared result parsing for the two function-judge languages, which
    both print a JSON results array between marker lines on stdout."""
    if proc.returncode != 0:
        err = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "Unknown error"
        return {"ok": False, "error": err, "results": []}

    stdout = proc.stdout
    if "__CB_RESULT_START__" not in stdout or "__CB_RESULT_END__" not in stdout:
        return {"ok": False, "error": "Could not read test results — did you rename the function?", "results": []}

    try:
        payload = stdout.split("__CB_RESULT_START__")[1].split("__CB_RESULT_END__")[0].strip()
        results = json.loads(payload)
    except (IndexError, ValueError):
        return {"ok": False, "error": "Could not parse test results.", "results": []}

    return {"ok": True, "error": None, "results": results}


# ======================================================================
#  C / C++ / JAVA — stdio judge (compile once, run once per test case)
# ======================================================================
_RUNTIME_NAMES = {"c": "gcc", "cpp": "g++", "java": "javac/java"}


def _run_stdio(language: str, code: str, test_cases_json: str):
    try:
        test_cases = json.loads(test_cases_json)
    except (TypeError, ValueError):
        test_cases = []

    with tempfile.TemporaryDirectory(prefix="cb_judge_") as tmpdir:
        try:
            run_cmd, compile_proc = _compile(language, code, tmpdir)
        except FileNotFoundError:
            return {"ok": False, "error": f"{_RUNTIME_NAMES[language]} isn't installed on this server. "
                                           f"Ask an admin to install it to enable this judge.", "results": []}
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Compilation timed out.", "results": []}

        if compile_proc.returncode != 0:
            err = (compile_proc.stderr or "Compilation failed.").strip()
            return {"ok": False, "error": err[:2000], "results": []}

        results = []
        for stdin_text, expected in test_cases:
            try:
                proc = subprocess.run(
                    run_cmd, input=stdin_text, capture_output=True, text=True,
                    timeout=TIMEOUT_SECONDS, cwd=tmpdir,
                )
            except subprocess.TimeoutExpired:
                results.append({"passed": False, "expected": expected, "actual": None,
                                 "error": f"Timed out (exceeded {TIMEOUT_SECONDS}s) — check for infinite loops."})
                continue

            actual = proc.stdout.strip()
            expected_norm = str(expected).strip()
            passed = actual == expected_norm
            entry = {"passed": passed, "expected": expected, "actual": actual}
            if not passed and proc.returncode != 0:
                stderr_lines = proc.stderr.strip().splitlines()
                entry["error"] = stderr_lines[-1] if stderr_lines else "Runtime error"
            results.append(entry)

        return {"ok": True, "error": None, "results": results}


def _compile(language: str, code: str, tmpdir: str):
    """Write + compile the submission. Returns (run_cmd, compile_proc)."""
    if language == "c":
        src_path = os.path.join(tmpdir, "main.c")
        bin_path = os.path.join(tmpdir, "main.out")
        with open(src_path, "w") as f:
            f.write(code)
        compile_proc = subprocess.run(
            ["gcc", src_path, "-O2", "-o", bin_path],
            capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS,
        )
        return [bin_path], compile_proc

    if language == "cpp":
        src_path = os.path.join(tmpdir, "main.cpp")
        bin_path = os.path.join(tmpdir, "main.out")
        with open(src_path, "w") as f:
            f.write(code)
        compile_proc = subprocess.run(
            ["g++", src_path, "-O2", "-std=c++17", "-o", bin_path],
            capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS,
        )
        return [bin_path], compile_proc

    if language == "java":
        src_path = os.path.join(tmpdir, "Main.java")
        with open(src_path, "w") as f:
            f.write(code)
        compile_proc = subprocess.run(
            ["javac", "Main.java"],
            capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS, cwd=tmpdir,
        )
        return ["java", "-cp", tmpdir, "Main"], compile_proc

    raise ValueError(f"unknown stdio language: {language}")
