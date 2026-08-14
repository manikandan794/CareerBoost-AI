"""Resume Builder (multi-step wizard + PDF export) and Resume Analyzer pages."""

import os
import json
import uuid

from flask import (
    Blueprint, render_template, request, session, redirect,
    url_for, flash, send_file, current_app, abort
)

from models.db import get_db
from utils.decorators import login_required
from utils.pdf_generator import generate_resume_pdf
from utils.resume_analyzer import analyze_resume

bp = Blueprint("resume", __name__)


@bp.route("/resume-builder", methods=["GET", "POST"])
@login_required
def builder():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        education = _zip_fields(request.form, ["edu_degree", "edu_institution", "edu_year", "edu_score"],
                                 ["degree", "institution", "year", "score"])
        experience = _zip_fields(request.form, ["exp_role", "exp_company", "exp_duration", "exp_description"],
                                  ["role", "company", "duration", "description"])
        projects = _zip_fields(request.form, ["proj_title", "proj_description"],
                                ["title", "description"])

        data = {
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "address": request.form.get("address", "").strip(),
            "linkedin": request.form.get("linkedin", "").strip(),
            "github": request.form.get("github", "").strip(),
            "portfolio": request.form.get("portfolio", "").strip(),
            "summary": request.form.get("summary", "").strip(),
            "skills": request.form.get("skills", "").strip(),
            "languages": request.form.get("languages", "").strip(),
            "certifications": request.form.get("certifications", "").strip(),
            "achievements": request.form.get("achievements", "").strip(),
            "education": json.dumps(education),
            "experience": json.dumps(experience),
            "projects": json.dumps(projects),
            "template": request.form.get("template", "classic"),
        }

        if not data["full_name"] or not data["email"]:
            flash("Full name and email are required.", "warning")
            return render_template("resume_builder.html", form_data=request.form)

        db.execute(
            """INSERT INTO resumes (user_id, full_name, email, phone, address, summary,
               skills, education, experience, projects, certifications, template)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                user_id, data["full_name"], data["email"], data["phone"], data["address"],
                data["summary"], data["skills"], data["education"], data["experience"],
                data["projects"], data["certifications"], data["template"],
            ),
        )
        db.commit()

        os.makedirs(current_app.config["RESUME_EXPORT_DIR"], exist_ok=True)
        filename = f"resume_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(current_app.config["RESUME_EXPORT_DIR"], filename)
        generate_resume_pdf(data, output_path)

        # Run the resume through the same analyzer used on the Analyzer page,
        # so the learner gets an instant ATS-style score before downloading.
        plain_text = _resume_to_plain_text(data, education, experience, projects)
        analysis = analyze_resume(plain_text)

        session["last_resume"] = {
            "filename": filename,
            "download_name": f"{data['full_name'] or 'resume'}_CareerBoost.pdf",
            "full_name": data["full_name"],
            "template": data["template"],
            "score": analysis["overall_score"],
            "tips": analysis["tips"][:3],
        }

        flash("Resume generated successfully!", "success")
        return redirect(url_for("resume.builder_success"))

    return render_template("resume_builder.html", form_data=None)


@bp.route("/resume-builder/success")
@login_required
def builder_success():
    last = session.get("last_resume")
    if not last:
        return redirect(url_for("resume.builder"))
    return render_template("resume_success.html", resume=last)


@bp.route("/resume-builder/download/<filename>")
@login_required
def download(filename):
    last = session.get("last_resume")
    if not last or last.get("filename") != filename:
        abort(403)
    output_path = os.path.join(current_app.config["RESUME_EXPORT_DIR"], filename)
    if not os.path.exists(output_path):
        abort(404)
    return send_file(output_path, as_attachment=True, download_name=last["download_name"])


@bp.route("/resume-analyzer", methods=["GET", "POST"])
@login_required
def analyzer():
    result = None
    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        job_description = request.form.get("job_description", "").strip()
        if len(resume_text) < 20:
            flash("Please paste your resume content (at least a few lines) to analyze.", "warning")
        else:
            result = analyze_resume(resume_text, job_description)
    return render_template("resume_analyzer.html", result=result)


def _zip_fields(form, field_names, keys):
    """
    Collect parallel repeated form fields (e.g. edu_degree[], edu_institution[])
    into a list of dicts, one dict per repeated form block. Rows where every
    value is blank are dropped.
    """
    lists = [form.getlist(name) for name in field_names]
    length = max((len(l) for l in lists), default=0)
    items = []
    for i in range(length):
        item = {keys[j]: (lists[j][i] if i < len(lists[j]) else "") for j in range(len(keys))}
        if any(v.strip() for v in item.values()):
            items.append(item)
    return items


def _resume_to_plain_text(data, education, experience, projects):
    """Flatten the structured resume data into plain text for the analyzer."""
    parts = [
        data.get("summary", ""),
        "Skills: " + data.get("skills", ""),
        "Education " + " ".join(f"{e.get('degree','')} {e.get('institution','')}" for e in education),
        "Experience " + " ".join(f"{e.get('role','')} {e.get('company','')} {e.get('description','')}" for e in experience),
        "Projects " + " ".join(f"{p.get('title','')} {p.get('description','')}" for p in projects),
        "Certifications: " + data.get("certifications", ""),
        "Achievements: " + data.get("achievements", ""),
    ]
    return "\n".join(p for p in parts if p.strip())
