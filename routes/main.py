"""Public-facing pages: landing page, about, contact."""

import re
import sqlite3

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from models.db import get_db

bp = Blueprint("main", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.route("/")
def home():
    db = get_db()
    stats = {
        "students": db.execute("SELECT COUNT(*) c FROM users WHERE is_admin = 0").fetchone()["c"],
        "companies": db.execute("SELECT COUNT(*) c FROM companies").fetchone()["c"],
        "questions": db.execute("SELECT COUNT(*) c FROM quiz_questions").fetchone()["c"]
        + db.execute("SELECT COUNT(*) c FROM interview_questions").fetchone()["c"],
        "problems": db.execute("SELECT COUNT(*) c FROM coding_problems").fetchone()["c"],
    }
    return render_template("index.html", stats=stats)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all required fields.", "danger")
            return render_template("contact.html", form=request.form)

        db = get_db()
        db.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message),
        )
        db.commit()
        flash("Thanks for reaching out! We'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form={})


@bp.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or request.form.get("email", "")).strip()

    if not email or not EMAIL_RE.match(email):
        return jsonify(success=False, message="Please enter a valid email address."), 400

    db = get_db()
    try:
        db.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify(success=False, message="You're already subscribed!"), 409

    return jsonify(success=True, message="Thanks for subscribing!")
