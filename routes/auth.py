"""Authentication routes: signup, login, logout, and opt-in Face Unlock."""

import json
import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from models.db import get_db
from utils.face_auth import (
    euclidean_distance, is_rate_limited, record_attempt, clear_attempts, is_valid_descriptor,
)

bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if len(full_name) < 2:
            errors.append("Please enter your full name.")
        if not EMAIL_RE.match(email):
            errors.append("Please enter a valid email address.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        if password != confirm:
            errors.append("Passwords do not match.")

        db = get_db()
        if not errors and db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone():
            errors.append("An account with this email already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("signup.html", form=request.form)

        db.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
            (full_name, email, generate_password_hash(password)),
        )
        db.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", form={})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            _login_user(user)
            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["is_admin"]:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


def _login_user(user):
    session.clear()
    session["user_id"] = user["id"]
    session["full_name"] = user["full_name"]
    session["is_admin"] = bool(user["is_admin"])


@bp.route("/face/check", methods=["POST"])
def face_check():
    """Does this email have Face Unlock enrolled? Used by the login page
    to decide whether to show the webcam capture UI. Always returns the
    same shape whether or not the account exists, so this endpoint can't
    be used to enumerate registered emails."""
    email = ((request.json or {}).get("email") or "").strip().lower()
    db = get_db()
    user = db.execute(
        "SELECT face_descriptor FROM users WHERE email = ?", (email,)
    ).fetchone()
    enrolled = bool(user and user["face_descriptor"])
    return jsonify({"enrolled": enrolled})


@bp.route("/face/verify", methods=["POST"])
def face_verify():
    """Log in via a face descriptor captured client-side by face-api.js.
    The client's own "is this a match" judgment is never trusted — the
    server re-computes the distance against the stored descriptor."""
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    descriptor = data.get("descriptor")

    max_attempts = current_app.config["FACE_MAX_ATTEMPTS"]
    window = current_app.config["FACE_ATTEMPT_WINDOW_SECONDS"]
    if not email or is_rate_limited(email, max_attempts, window):
        return jsonify({"ok": False, "error": "Too many face-login attempts. Please wait a few minutes "
                                               "or log in with your password instead."}), 429

    if not is_valid_descriptor(descriptor):
        return jsonify({"ok": False, "error": "Couldn't read a face from the camera. Try again with better "
                                               "lighting, facing the camera directly."}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    record_attempt(email)

    if not user or not user["face_descriptor"]:
        return jsonify({"ok": False, "error": "Face Unlock isn't set up for this account yet."}), 400

    stored = json.loads(user["face_descriptor"])
    distance = euclidean_distance(stored, descriptor)
    threshold = current_app.config["FACE_MATCH_THRESHOLD"]

    if distance > threshold:
        return jsonify({"ok": False, "error": "Face didn't match closely enough. Try again, or log in "
                                               "with your password."}), 401

    clear_attempts(email)
    _login_user(user)
    flash(f"Welcome back, {user['full_name']}! (Signed in with Face Unlock)", "success")
    return jsonify({"ok": True, "redirect": url_for("admin.dashboard") if user["is_admin"] else url_for("dashboard.index")})


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
