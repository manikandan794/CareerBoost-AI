"""User profile: view and edit personal / academic details, plus opt-in Face Unlock enrollment."""

import json
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify

from models.db import get_db
from utils.decorators import login_required
from utils.face_auth import is_valid_descriptor

bp = Blueprint("profile", __name__)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def index():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        college = request.form.get("college", "").strip()
        branch = request.form.get("branch", "").strip()
        graduation_year = request.form.get("graduation_year", "").strip()
        bio = request.form.get("bio", "").strip()

        db.execute(
            """UPDATE users SET full_name=?, phone=?, college=?, branch=?,
               graduation_year=?, bio=? WHERE id=?""",
            (full_name, phone, college, branch, graduation_year, bio, user_id),
        )
        db.commit()
        session["full_name"] = full_name
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.index"))

    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    resumes = db.execute(
        "SELECT * FROM resumes WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    ).fetchall()
    quiz_count = db.execute(
        "SELECT COUNT(*) c FROM quiz_results WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]

    return render_template("profile.html", user=user, resumes=resumes, quiz_count=quiz_count)


@bp.route("/profile/face/enroll", methods=["POST"])
@login_required
def face_enroll():
    """Store a face-api.js descriptor captured client-side for the logged-in
    user, so they can use Face Unlock on future logins. Requires the user
    to already be signed in with their password — enrollment can't itself
    be used to create account access."""
    descriptor = (request.json or {}).get("descriptor")
    if not is_valid_descriptor(descriptor):
        return jsonify({"ok": False, "error": "Couldn't read a clear face from the camera. "
                                               "Try again with better lighting, facing the camera directly."}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET face_descriptor = ?, face_enrolled_at = CURRENT_TIMESTAMP WHERE id = ?",
        (json.dumps(descriptor), session["user_id"]),
    )
    db.commit()
    return jsonify({"ok": True})


@bp.route("/profile/face/remove", methods=["POST"])
@login_required
def face_remove():
    db = get_db()
    db.execute(
        "UPDATE users SET face_descriptor = NULL, face_enrolled_at = NULL WHERE id = ?",
        (session["user_id"],),
    )
    db.commit()
    return jsonify({"ok": True})
