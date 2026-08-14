"""Company List: browse hiring companies and eligibility criteria."""

from flask import Blueprint, render_template, request

from models.db import get_db
from utils.decorators import login_required

bp = Blueprint("companies", __name__)


@bp.route("/companies")
@login_required
def index():
    db = get_db()
    search = request.args.get("q", "").strip()

    if search:
        rows = db.execute(
            "SELECT * FROM companies WHERE name LIKE ? OR industry LIKE ? ORDER BY name",
            (f"%{search}%", f"%{search}%"),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM companies ORDER BY name").fetchall()

    return render_template("companies.html", companies=rows, search=search)
