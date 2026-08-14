# CareerBoost AI — Placement Preparation Platform

A full-stack placement preparation platform built with **Flask, SQLite, Bootstrap 5,
and vanilla JavaScript**. Includes authentication, a professional multi-step resume
builder (4 templates, live preview, PDF export + instant ATS score), a resume
analyzer, a 110-question aptitude quiz bank (Easy/Medium/Hard across Quantitative,
Logical, Verbal & Technical), 100 technical + HR interview questions, a coding
practice judge across **Python, JavaScript, C, C++, Java and HTML/CSS** with a real
in-browser editor that grades your code against test cases (or renders a live
preview for HTML/CSS), a company directory, user profiles with optional **Face
Unlock** login, an admin dashboard, and a page-aware **AI Assistant** chat widget —
all wrapped in a responsive, animated, dark/light-mode UI.

### What's new
- **110 aptitude quiz questions** (Quantitative / Logical / Verbal / Technical ×
  Easy / Medium / Hard) with a difficulty picker and a "review your mistakes" screen.
- **100 interview questions** across Python, OOP, DBMS, SQL, CS Fundamentals, OS,
  Networks, Web Dev, Java and HR — filterable by category *and* difficulty.
- **52 coding problems across 6 languages** — Python & JavaScript are graded by
  calling your function directly; C, C++ & Java are graded by compiling your full
  program and comparing stdin/stdout; HTML/CSS problems render a live preview
  instead (there's no single "correct" markup to auto-grade). Filter Coding
  Practice by language, difficulty or topic. See "Coding judge requirements" below.
- **Professional Resume Builder v2** — a 7-step guided wizard (Basics → Summary &
  Skills → Education → Experience → Projects → Extras → Template), a live preview
  pane, 4 PDF templates (Classic/Modern/Minimal/Executive), LinkedIn/GitHub/portfolio
  links, languages & achievements, and an instant ATS-readiness score after generating.
- **AI Assistant** — a floating chat widget on every page that knows which page
  (and, on Coding Practice, which *language*) you're on and coaches you through it.
  Works out of the box with a built-in rule-based engine covering language-specific
  gotchas for all six languages; optionally upgrades to real Claude responses if you
  set an `ANTHROPIC_API_KEY` env var and `pip install anthropic`.
- **Face Unlock (opt-in)** — after your first password login, enroll your face from
  the Profile page and use your webcam to sign in next time. See "Face Unlock" below
  for how it works and its limitations.

## Tech Stack
- **Backend:** Python 3, Flask (Blueprints), SQLite (raw SQL, no ORM)
- **Frontend:** HTML5, CSS3 (custom design system via CSS variables), Bootstrap 5,
  Bootstrap Icons, Chart.js, CodeMirror 5, vanilla JavaScript, face-api.js (Face Unlock only)
- **PDF generation:** ReportLab
- **Code judges:** sandboxed subprocess execution with a timeout + a denylist of
  risky calls per language; C/C++/Java are compiled on the fly and run once per test case
- **Auth:** Session-based, passwords hashed with Werkzeug's `generate_password_hash`;
  Face Unlock is an additional opt-in factor, never a replacement for the password

## Folder Structure
```
careerboost-ai/
├── app.py                 # App factory, blueprint registration
├── config.py               # Central configuration
├── requirements.txt
├── database/
│   ├── schema.sql          # Table definitions (SQLite auto-created on first run)
│   └── seed_data.py         # 110 quiz Qs, 100 interview Qs, 30 coding problems
├── models/
│   └── db.py                # Connection helper + demo data seeding
├── routes/                  # One blueprint per feature area
│   ├── auth.py               # signup / login / logout
│   ├── main.py                # home / about / contact
│   ├── dashboard.py            # user dashboard + chart data API
│   ├── resume.py                # resume builder wizard (PDF export) + analyzer
│   ├── quiz.py                   # aptitude quiz
│   ├── interview.py               # technical interview questions
│   ├── coding.py                   # coding practice problems + code judge API
│   ├── companies.py                 # company directory
│   ├── profile.py                    # user profile
│   ├── admin.py                       # admin dashboard
│   ├── assistant.py                    # AI Assistant chat API
│   ├── ai_coach.py                      # AI Career Coach hub (roadmap, skill gap, study, quiz gen, resume match, company prep, mock interview)
│   └── gd.py                             # Group Discussion module (topics, live simulation, evaluation, history)
├── utils/
│   ├── decorators.py         # @login_required / @admin_required
│   ├── pdf_generator.py       # ReportLab resume PDF builder (4 templates)
│   ├── resume_analyzer.py      # keyword/ATS-style resume scoring
│   ├── code_runner.py           # sandboxed Python code judge
│   ├── ai_engine.py              # AI Assistant widget (Gemini-backed + rule-based fallback)
│   ├── gemini_service.py          # low-level Gemini REST API wrapper (the only place that calls Gemini)
│   └── ai_tasks.py                 # one prompt-builder per AI capability, built on gemini_service
├── static/
│   ├── css/style.css           # design system, dark/light theme, animations
│   ├── js/theme.js              # dark/light mode toggle (localStorage)
│   ├── js/main.js                # shared UI behaviour (quiz timer, form blocks, etc.)
│   └── generated/                 # resume PDFs are temporarily written here
└── templates/
    ├── base.html               # layout shell
    ├── components/               # navbar.html, footer.html (reusable partials)
    ├── errors/                     # 404.html, 403.html
    └── *.html                       # one template per page
```

## Getting Started

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (required — the app won't start
#    without SECRET_KEY, DEFAULT_ADMIN_EMAIL and DEFAULT_ADMIN_PASSWORD)
cp .env.example .env
# then edit .env: set SECRET_KEY, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD,
# and add your GEMINI_API_KEY for the AI features

# 4. Run the app
python app.py
```

Open **http://127.0.0.1:5000** in your browser. `.env` is loaded
automatically via `python-dotenv` — no need to `export` variables by hand.
If `SECRET_KEY`, `DEFAULT_ADMIN_EMAIL` or `DEFAULT_ADMIN_PASSWORD` are
missing, the app will refuse to start and print a clear configuration
error instead of falling back to an insecure default.

The SQLite database (`database/careerboost.db`) and all demo content
(aptitude questions, companies, interview questions, coding problems) are
created and seeded automatically on first run — no manual setup needed.

## Admin Account
There is no built-in/default admin account. The first time the database
is created, an admin user is seeded using whatever email and password you
set for `DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD` in your `.env`
file — use a real email you control and a strong, unique password.
| Role    | Email                        | Password                  |
|---------|-------------------------------|----------------------------|
| Admin   | *(from `DEFAULT_ADMIN_EMAIL`)* | *(from `DEFAULT_ADMIN_PASSWORD`)* |
| Student | *(sign up your own)*         | —                          |

## Feature Notes
- **Dark/Light mode** is applied instantly on load (no flash of wrong theme) and
  persisted in `localStorage`.
- **Resume Builder** supports dynamically repeatable Education / Experience /
  Project blocks and exports a clean, ATS-friendly one-page PDF via ReportLab.
- **Resume Analyzer** is fully self-contained (no external AI calls) — it scores
  resumes on section completeness, action-verb usage, length, and keyword overlap
  against an optional job description.
- **Aptitude Quiz** picks 10 random questions per category and includes a
  10-minute countdown timer that auto-submits.
- **Admin Dashboard** shows platform-wide stats, signup/quiz charts, recent
  students, and contact messages.

### Coding judge requirements
Each language's judge needs its runtime installed on the machine running Flask
(nothing extra is needed on the learner's browser beyond CodeMirror, already
bundled). If a runtime is missing, that language's problems return a clear
"not installed" error instead of crashing:

| Language   | Requires on the server      |
|------------|------------------------------|
| Python     | Nothing extra (same interpreter running Flask) |
| JavaScript | `node` on PATH               |
| C          | `gcc` on PATH                |
| C++        | `g++` on PATH (C++17)        |
| Java       | `javac` **and** `java` on PATH |
| HTML/CSS   | Nothing — rendered client-side in a sandboxed iframe |

None of these judges are hardened multi-tenant sandboxes (no containers/
seccomp/cgroups) — they're a denylist + timeout, appropriate for a single
trusted host running a student practice tool, not for exposing to arbitrary
untrusted internet traffic without further isolation.

### Face Unlock
An **opt-in** alternative to typing your password on return visits:
1. Log in normally with your password at least once.
2. On your Profile page, click **Set Up Face Unlock** — this uses face-api.js
   (running entirely in your browser) to turn a webcam frame into a 128-number
   descriptor, which is sent to the server and stored against your account.
3. On future visits, click **Login with Face Unlock**, enter your email, and
   scan — the server re-computes the match itself server-side (it never trusts
   a client-reported "yes, matched").

**Limitations to know before relying on this:**
- No liveness detection — a clear photo/video could potentially fool it. Treat
  it as a convenience, not a hardened biometric security system.
- Requires camera access and reasonable lighting; accuracy depends on the
  browser's face-api.js model.
- Face-login attempts are rate-limited per email (5 attempts / 5 minutes,
  configurable in `config.py`) — but that limiter is in-memory and per-process,
  so it resets on restart and won't be shared across multiple Gunicorn/uWSGI
  workers. Swap in a Redis- or DB-backed limiter before running this behind
  multiple workers in production.
- Model files load from a public CDN (`cdn.jsdelivr.net`); self-host them for
  a production deployment instead of depending on a third party.
- A user can always fall back to their password — Face Unlock never replaces it.

## Production Notes
The app now defaults to production-safe settings (debug off, host
`0.0.0.0`, port from `$PORT`) — see "Cloud Deployment" below. A few things
to still decide per deployment:
- `SECRET_KEY`, `DEFAULT_ADMIN_EMAIL` and `DEFAULT_ADMIN_PASSWORD` are
  required environment variables — there is no default/fallback value for
  any of them, and the app will refuse to start with a clear
  configuration error if one is missing. Set a strong, random
  `SECRET_KEY`, and a real admin email you control with a strong, unique
  `DEFAULT_ADMIN_PASSWORD`, before your first deploy.
- SQLite is fine for a demo/small deployment (see the note below on disk
  persistence); consider PostgreSQL/MySQL if you need concurrent writers
  or guaranteed durability across restarts
- Install the compilers/runtimes listed above (`gcc`, `g++`, `javac`/`java`,
  `node`) on the host for whichever coding languages you want auto-graded;
  languages whose runtime isn't present show a clear "not installed"
  message instead of failing
- Replace the in-memory Face Unlock rate limiter with a shared store
  (e.g. Redis) if you run multiple Gunicorn workers/dynos, since each
  worker currently tracks attempts independently

## Cloud Deployment

The app is ready to deploy to any platform that runs a Python web
process from a Git repository (Render, Railway, Fly.io, Heroku-style
platforms, a VPS, etc.). The steps are generic on purpose — plug in your
platform's specific UI/CLI where noted.

1. **Push the project to GitHub.**
   ```bash
   git init
   git add .
   git commit -m "CareerBoost AI - cloud deployment ready"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPOSITORY_URL
   git push -u origin main
   ```
   `.env` is excluded by `.gitignore`, so your real Gemini key and secret
   key never leave your machine.

2. **Create a new web service** on your chosen platform and connect it to
   this GitHub repository.

3. **Select a Python environment** (Python 3.11+ recommended — matches
   what this project was built/tested against).

4. **Install dependencies** from `requirements.txt` — most platforms do
   this automatically once they detect the file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables** on the platform (do NOT put real
   values in any file that gets committed):
   | Variable | Required | Notes |
   |---|---|---|
   | `SECRET_KEY` | Yes | Long random string — signs session cookies |
   | `GEMINI_API_KEY` | Yes, for AI features | From https://aistudio.google.com/app/apikey |
   | `GEMINI_MODEL` | No | Defaults to `gemini-2.0-flash` |
   | `DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD` | Yes | Credentials for the admin account created on first run — no default value |
   | `PORT` | Usually automatic | Most platforms set this for you; the app reads it via `os.environ.get("PORT")` |

6. **Configure the production start command.** This project ships a
   `Procfile`:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```
   Platforms that read a `Procfile` automatically will pick this up; on
   platforms that ask for a start command explicitly, use the same line
   (minus the `web:` prefix): `gunicorn app:app --bind 0.0.0.0:$PORT`.

7. **Deploy.** The first request boots the app, which creates
   `database/careerboost.db` and `static/generated/` automatically if
   they don't exist, then seeds demo content (quiz questions, companies,
   interview questions, coding problems, GD topics) into the empty
   database — no manual migration step required.

8. **Test the live URL.** Confirm the home page loads, sign up a test
   account, and (if `GEMINI_API_KEY` is set) try one AI feature such as
   the AI Career Roadmap or Group Discussion simulator.

### A note on SQLite and cloud filesystems
SQLite is a great fit for this project's size and for demos, and the app
manages the database file for you. However, **some cloud platforms use an
ephemeral filesystem** — anything written to disk (including
`database/careerboost.db` and generated resume PDFs) can be wiped on
redeploys, restarts, or when scaling to multiple instances, unless the
platform is configured with a persistent disk/volume mounted at the
project directory. This is a platform-level setting, not something the
app can control. If your chosen platform offers persistent disks,
mount one and point `DATABASE_PATH` at it (or keep the default project
path if the whole project directory already lives on the persistent
disk). Do not assume SQLite data survives indefinitely on every
platform by default — check your provider's docs on persistent storage.

---

## 🤖 Gemini AI Upgrade — AI Career Coach + Group Discussion

This upgrade adds a full Gemini-powered AI layer on top of the existing app
**without changing or removing any existing feature.** Login/signup, dashboard,
resume builder + PDF export, resume analyzer, aptitude quiz, interview
questions, coding practice, company directory, profile, admin dashboard, and
the original AI Assistant widget all continue to work exactly as before —
the widget now simply prefers Gemini when configured, and quietly falls back
to its original rule-based coaching when it isn't.

### 1. Install & configure
```bash
pip install -r requirements.txt      # adds `requests`, used to call the Gemini REST API

# Get a free key: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="your-key-here"     # macOS/Linux
setx GEMINI_API_KEY "your-key-here"       # Windows (restart your terminal after)

python app.py
```
Copy `.env.example` to `.env` (or export the variables yourself) — see that
file for the full list. **Nothing else needs to change.** If `GEMINI_API_KEY`
is not set, every new AI page shows a clear "AI features aren't configured
yet" notice instead of failing, and the rest of the platform is unaffected.

### 2. New environment variables
| Variable         | Required | Purpose                                              |
|-------------------|----------|-------------------------------------------------------|
| `GEMINI_API_KEY`  | Yes, for AI features | Gemini API key. Never hard-coded, never sent to the frontend. |
| `GEMINI_MODEL`    | No       | Overrides the model (defaults to `gemini-2.0-flash`). |

### 3. New/modified files
**New — Gemini architecture**
- `utils/gemini_service.py` — the ONLY place that calls the Gemini REST API. Handles missing/invalid keys, timeouts, rate limits, 5xx errors, safety blocks, and malformed JSON — every public function returns a `GeminiResult(ok, text/data, error)` instead of raising, so a failure anywhere always surfaces a friendly message, never a stack trace.
- `utils/ai_tasks.py` — one prompt-builder function per AI capability (career roadmap, skill gap, study assistant, quiz generator, resume↔JD match, company prep, mock interview Q&A + report, coding assist, Group Discussion participant turns + evaluation), all built on `gemini_service`.

**New — routes**
- `routes/ai_coach.py` — `/ai` hub + `/ai/roadmap`, `/ai/skill-gap`, `/ai/study`, `/ai/quiz-generator`, `/ai/resume-match`, `/ai/company-prep`, `/ai/interview-coach` pages, plus their `/api/ai/...` JSON endpoints.
- `routes/gd.py` — `/gd` dashboard, `/gd/topics`, `/gd/session/<id>` (live simulation), `/gd/result/<id>`, `/gd/history`, plus `/api/gd/<id>/message|tip|end`.

**New — templates**
`templates/ai_hub.html`, `ai_roadmap.html`, `ai_skill_gap.html`, `ai_study.html`,
`ai_quiz_generator.html`, `ai_resume_match.html`, `ai_company_prep.html`,
`ai_interview_coach.html`, `gd_home.html`, `gd_topics.html`, `gd_session.html`,
`gd_result.html`, `gd_history.html`, plus `templates/components/ai_not_configured.html`
(shared warning banner).

**Modified**
- `utils/ai_engine.py` — the original floating AI Assistant now prefers Gemini (via `ai_tasks.assistant_reply`) when `GEMINI_API_KEY` is set, and falls back to its original rule-based engine otherwise. Page-context labels extended for the new AI/GD pages.
- `static/js/assistant.js` — extended `ENDPOINT_TO_PAGE` / suggested-prompt maps so the floating widget knows it's on an AI tool or GD page.
- `database/schema.sql` — 9 new tables (see below); every existing table is untouched.
- `database/seed_data.py` — added `GD_TOPICS` (30 Group Discussion topics across Technology / Education / Society / Business / Abstract categories).
- `models/db.py` — seeds `gd_topics` on first run alongside the existing quiz/interview/coding/company seed data.
- `routes/admin.py` + `templates/admin.html` — added AI usage stats (total AI requests, GD attempts, avg GD score, AI quiz attempts, roadmaps generated, most-practiced GD topic).
- `templates/dashboard.html` — added a Quick Actions row linking to AI Career Coach, Mock Interview, Practice GD, etc.
- `templates/components/navbar.html` — added an "AI Coach" dropdown linking every new tool + Group Discussion.
- `requirements.txt` — added `requests` (used for the Gemini REST calls).
- **Color palette** — the UI's teal/amber design system (`static/css/style.css` CSS variables) replaced the previous indigo/blue palette everywhere (cards, badges, chart colors, gradients) for a more distinctive look; every color still routes through the same `--primary`/`--accent`/etc. CSS variables so dark/light mode continues to work unchanged.

### 4. Database changes
All additive — no existing table was altered or dropped. New tables:

| Table | Purpose |
|---|---|
| `ai_conversations`, `ai_messages` | Generic turn-based AI chat log — currently used by the Mock Interview Coach; reusable by future chat-style tools. |
| `career_roadmaps` | Saved AI Career Roadmap results per user. |
| `skill_gap_reports` | Saved AI Skill Gap Analyzer results per user. |
| `ai_quiz_attempts` | AI-generated quiz attempts + scores + weak topics. |
| `gd_topics` | Seeded Group Discussion topic bank (category, title, difficulty, description). |
| `gd_sessions` | One row per GD practice session (topic, difficulty, participant count, status). |
| `gd_messages` | Every message in a GD session, tagged by speaker (`You`, `Participant A/B/C/D`). |
| `gd_evaluations` | Final Gemini-scored evaluation per session (12 category scores + qualitative feedback). |

### 5. Feature architecture (request flow)
```
Browser (fetch/JS)
   │  POST /api/ai/<tool>  or  /api/gd/<id>/<action>
   ▼
Flask route (routes/ai_coach.py or routes/gd.py)
   │  - @login_required, input validation
   │  - calls one function in utils/ai_tasks.py
   ▼
utils/ai_tasks.py           (prompt construction, one function per AI task)
   │  calls
   ▼
utils/gemini_service.py     (the only HTTP call to Gemini; timeouts/retries/error mapping)
   │  requests.post(...)
   ▼
Gemini API  →  JSON/text response
   ▲
   │  GeminiResult(ok, text/data, error) bubbles back up
Flask route  →  saves relevant history row (SQLite) → returns JSON
   │
   ▼
Browser JS renders the result into cards/timelines/chat bubbles (no page reload)
```

### 6. What was intentionally scoped for this pass
Given the breadth of the original spec (a 28-section, full-platform request),
this pass prioritized shipping every listed AI capability as a genuinely
working, end-to-end feature — Gemini service layer, AI Career Coach (roadmap,
skill gap, study assistant, quiz generator, resume↔JD match, company prep,
mock interview with scoring), and the full Group Discussion module
(topics → live AI-simulated session → Gemini evaluation → history) — over
adding extra static seed content or a bespoke UI treatment for every AI
sub-feature. Two follow-ups worth doing next if you want to go further:
- Wire an "Ask AI" button directly into the existing Coding Practice page UI (the backend endpoint `/api/ai/coding-assist` already exists and is ready to call).
- Add readiness-score aggregation (resume/interview/coding/aptitude/GD) to the student dashboard's "Career Progress" section — the underlying data (quiz_results, gd_evaluations, ai_quiz_attempts, etc.) is already there to compute it from.

### 7. Testing performed
- Verified `database/schema.sql` executes cleanly and every new table is created.
- Booted the full Flask app and confirmed all 59+ routes register with no import errors.
- End-to-end tested (via Flask's test client, with Gemini responses mocked to avoid needing network access in this environment): signup → login → dashboard → AI Roadmap generation → Skill Gap analysis → AI Quiz generate/submit → full Group Discussion flow (start → message → end → evaluated result → history) → Mock Interview start. All returned correct JSON/HTML with no server errors.
- Confirmed AI pages degrade gracefully (clear "not configured" message, HTTP 502 with a friendly JSON error) when `GEMINI_API_KEY` is unset, rather than crashing.

