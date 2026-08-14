"""
Lightweight SQLite data access layer.

We intentionally avoid a heavy ORM here so the codebase stays easy
to read for learners while remaining production-clean:
 - get_db()      -> per-request connection (row objects behave like dicts)
 - init_db()     -> creates tables from schema.sql (idempotent)
 - seed_db()     -> inserts demo content the first time the app runs
"""

import os
import sqlite3
import json
from flask import g, current_app
from werkzeug.security import generate_password_hash

from database.seed_data import (
    QUIZ_QUESTIONS,
    INTERVIEW_QUESTIONS,
    CODING_PROBLEMS,
    COMPANIES,
    GD_TOPICS,
)


def get_db():
    """Return a SQLite connection stored on Flask's app context `g`."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables (if they do not already exist) and seed demo data."""
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(app.config["DATABASE_PATH"]), "schema.sql")
        with open(schema_path, "r") as f:
            db.executescript(f.read())
        db.commit()
        _migrate_columns(db)
        _seed_db(app, db)


def _migrate_columns(db):
    """Add any columns introduced after a database file already existed."""
    def _ensure(table, column, ddl):
        cols = [r["name"] for r in db.execute(f"PRAGMA table_info({table})").fetchall()]
        if column not in cols:
            db.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")

    _ensure("interview_questions", "difficulty", "difficulty TEXT DEFAULT 'Medium'")
    _ensure("coding_problems", "function_name", "function_name TEXT")
    _ensure("coding_problems", "starter_code", "starter_code TEXT")
    _ensure("coding_problems", "test_cases", "test_cases TEXT")
    _ensure("coding_problems", "hints", "hints TEXT")
    _ensure("coding_problems", "language", "language TEXT DEFAULT 'python'")
    _ensure("coding_problems", "judge_type", "judge_type TEXT DEFAULT 'function'")
    _ensure("users", "face_descriptor", "face_descriptor TEXT")
    _ensure("users", "face_enrolled_at", "face_enrolled_at TIMESTAMP")
    db.commit()


def _seed_db(app, db):
    """Populate demo/reference content only if tables are empty."""

    # ---- Default admin account -------------------------------------
    admin = db.execute(
        "SELECT id FROM users WHERE email = ?", (app.config["DEFAULT_ADMIN_EMAIL"],)
    ).fetchone()
    if not admin:
        db.execute(
            """INSERT INTO users (full_name, email, password_hash, is_admin)
               VALUES (?, ?, ?, 1)""",
            (
                "Platform Admin",
                app.config["DEFAULT_ADMIN_EMAIL"],
                generate_password_hash(app.config["DEFAULT_ADMIN_PASSWORD"]),
            ),
        )

    # ---- Aptitude quiz questions --------------------------------------
    quiz_count = db.execute("SELECT COUNT(*) c FROM quiz_questions").fetchone()["c"]
    if quiz_count < len(QUIZ_QUESTIONS):
        db.execute("DELETE FROM quiz_questions")
        db.executemany(
            """INSERT INTO quiz_questions
               (category, difficulty, question, option_a, option_b, option_c, option_d, correct_option)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            QUIZ_QUESTIONS,
        )

    # ---- Companies -------------------------------------------------
    if db.execute("SELECT COUNT(*) c FROM companies").fetchone()["c"] == 0:
        db.executemany(
            """INSERT INTO companies (name, industry, role, package, location, eligibility, logo_icon)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            COMPANIES,
        )

    # ---- Interview questions ----------------------------------------
    interview_count = db.execute("SELECT COUNT(*) c FROM interview_questions").fetchone()["c"]
    if interview_count < len(INTERVIEW_QUESTIONS):
        db.execute("DELETE FROM interview_questions")
        db.executemany(
            "INSERT INTO interview_questions (category, difficulty, question, answer) VALUES (?, ?, ?, ?)",
            INTERVIEW_QUESTIONS,
        )

    # ---- Coding problems ---------------------------------------------
    coding_count = db.execute("SELECT COUNT(*) c FROM coding_problems").fetchone()["c"]
    if coding_count < len(CODING_PROBLEMS):
        db.execute("DELETE FROM coding_problems")
        db.executemany(
            """INSERT INTO coding_problems
               (title, difficulty, topic, description, sample_input, sample_output,
                function_name, starter_code, test_cases, hints, language, judge_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            CODING_PROBLEMS,
        )

    # ---- Group Discussion topics --------------------------------------
    gd_topic_count = db.execute("SELECT COUNT(*) c FROM gd_topics").fetchone()["c"]
    if gd_topic_count < len(GD_TOPICS):
        db.execute("DELETE FROM gd_topics")
        db.executemany(
            "INSERT INTO gd_topics (category, title, difficulty, description) VALUES (?, ?, ?, ?)",
            GD_TOPICS,
        )

    db.commit()
