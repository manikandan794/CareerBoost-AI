-- ============================================================
--  CareerBoost AI  —  SQLite Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone         TEXT,
    college       TEXT,
    branch        TEXT,
    graduation_year TEXT,
    bio           TEXT,
    is_admin      INTEGER DEFAULT 0,
    face_descriptor TEXT,        -- JSON array (128-d face-api.js descriptor); NULL = not enrolled
    face_enrolled_at TIMESTAMP,  -- when the face was registered
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    full_name   TEXT,
    email       TEXT,
    phone       TEXT,
    address     TEXT,
    summary     TEXT,
    skills      TEXT,      -- comma separated
    education   TEXT,      -- JSON string
    experience  TEXT,      -- JSON string
    projects    TEXT,      -- JSON string
    certifications TEXT,
    template    TEXT DEFAULT 'classic',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT NOT NULL,        -- Quantitative / Logical / Verbal
    difficulty  TEXT DEFAULT 'Medium',
    question    TEXT NOT NULL,
    option_a    TEXT NOT NULL,
    option_b    TEXT NOT NULL,
    option_c    TEXT NOT NULL,
    option_d    TEXT NOT NULL,
    correct_option TEXT NOT NULL      -- 'A' | 'B' | 'C' | 'D'
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    category    TEXT,
    score       INTEGER,
    total       INTEGER,
    taken_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS companies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    industry    TEXT,
    role        TEXT,
    package     TEXT,
    location    TEXT,
    eligibility TEXT,
    logo_icon   TEXT DEFAULT 'bi-building'
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    subject     TEXT,
    message     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS subscribers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coding_problems (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    difficulty  TEXT DEFAULT 'Easy',
    topic       TEXT,
    description TEXT,
    sample_input  TEXT,
    sample_output TEXT,
    function_name TEXT,          -- name of the function the user must implement
    starter_code  TEXT,          -- pre-filled Python starter code shown in the editor
    test_cases    TEXT,          -- JSON test cases (shape depends on judge_type)
    hints         TEXT,          -- JSON list of progressive hints (easy -> spoiler)
    language      TEXT DEFAULT 'python',  -- python | javascript | c | cpp | java | html_css
    judge_type    TEXT DEFAULT 'function' -- 'function' (call fn, compare return),
                                           -- 'stdio' (compile, compare stdout),
                                           -- 'preview' (HTML/CSS, no auto-grading)
);

CREATE TABLE IF NOT EXISTS interview_questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT NOT NULL,   -- e.g. Python, DBMS, OOP, CS Fundamentals
    difficulty  TEXT DEFAULT 'Medium',
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activity_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    action      TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================================
--  AI Career Coach + Group Discussion  (added for the Gemini
--  competition-level upgrade — see routes/ai_coach.py, routes/gd.py)
-- ============================================================

-- Generic conversation log used by chat-style AI tools (Mock Interview
-- Coach today; reusable by any future turn-based AI feature) so we
-- don't need a bespoke table per tool.
CREATE TABLE IF NOT EXISTS ai_conversations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    tool        TEXT NOT NULL,        -- 'interview_coach', etc.
    meta        TEXT,                 -- JSON: category/mode/question_number/etc.
    status      TEXT DEFAULT 'active',-- active | completed
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role            TEXT NOT NULL,     -- 'user' | 'assistant'
    content         TEXT NOT NULL,
    meta            TEXT,              -- optional JSON (score, strengths, ...)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id)
);
CREATE INDEX IF NOT EXISTS idx_ai_messages_conv ON ai_messages(conversation_id);

CREATE TABLE IF NOT EXISTS career_roadmaps (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    target_role     TEXT,
    education_level TEXT,
    current_skills  TEXT,
    experience_level TEXT,
    study_time      TEXT,
    preferred_tech  TEXT,
    roadmap_json    TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS skill_gap_reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    target_role     TEXT,
    current_skills  TEXT,
    report_json     TEXT NOT NULL,
    readiness_percent INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_quiz_attempts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    subject         TEXT,
    topic           TEXT,
    difficulty      TEXT,
    questions_json  TEXT NOT NULL,
    score           INTEGER,
    total           INTEGER,
    weak_topics     TEXT,
    taken_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS gd_topics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT NOT NULL,     -- Technology / Education / Society / Business / Abstract
    title       TEXT NOT NULL,
    difficulty  TEXT DEFAULT 'Medium',
    description TEXT
);

CREATE TABLE IF NOT EXISTS gd_sessions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL,
    topic_id            INTEGER,
    topic_title         TEXT NOT NULL,
    difficulty          TEXT DEFAULT 'Medium',
    participant_count   INTEGER DEFAULT 3,
    time_limit_minutes  INTEGER DEFAULT 10,
    status              TEXT DEFAULT 'active',   -- active | completed
    started_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at            TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES gd_topics(id)
);

CREATE TABLE IF NOT EXISTS gd_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    speaker     TEXT NOT NULL,     -- 'You' | 'Participant A' | 'Participant B' ...
    message     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES gd_sessions(id)
);
CREATE INDEX IF NOT EXISTS idx_gd_messages_session ON gd_messages(session_id);

CREATE TABLE IF NOT EXISTS gd_evaluations (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id                  INTEGER NOT NULL UNIQUE,
    user_id                     INTEGER NOT NULL,
    overall_score               INTEGER,
    communication_score         INTEGER,
    relevance_score             INTEGER,
    clarity_score               INTEGER,
    confidence_score            INTEGER,
    topic_knowledge_score       INTEGER,
    logical_thinking_score      INTEGER,
    listening_score             INTEGER,
    leadership_score            INTEGER,
    team_participation_score    INTEGER,
    vocabulary_score            INTEGER,
    structure_score             INTEGER,
    strong_points                TEXT,   -- JSON list
    weak_points                  TEXT,   -- JSON list
    mistakes                     TEXT,   -- JSON list
    better_alternatives          TEXT,   -- JSON list
    improvement_plan             TEXT,   -- JSON list
    created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES gd_sessions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
