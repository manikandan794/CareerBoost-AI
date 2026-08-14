"""
Generates a clean, ATS-friendly resume PDF from form data using ReportLab.
Kept separate from route logic so it can be unit-tested or reused.

Supports four visual templates (selected via data['template']):
  classic    — traditional centered header, indigo accents (safest for ATS)
  modern     — left accent bar, teal/cyan accents
  minimal    — no color, pure black & white, most conservative
  executive  — dark navy header block, serif-leaning body
"""

import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

TEMPLATES = {
    "classic":   {"accent": "#4338CA", "name_align": TA_LEFT,   "header_bg": None},
    "modern":    {"accent": "#0891B2", "name_align": TA_LEFT,   "header_bg": None},
    "minimal":   {"accent": "#111111", "name_align": TA_LEFT,   "header_bg": None},
    "executive": {"accent": "#1E1B2E", "name_align": TA_CENTER, "header_bg": "#1E1B2E"},
}


def generate_resume_pdf(data: dict, output_path: str):
    """
    data keys: full_name, email, phone, address, summary, skills (str),
               linkedin, github, portfolio, languages,
               education (list[dict]), experience (list[dict]),
               projects (list[dict]), certifications, achievements,
               template
    """
    theme = TEMPLATES.get(data.get("template", "classic"), TEMPLATES["classic"])
    accent = colors.HexColor(theme["accent"])

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=16 * mm, bottomMargin=14 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "NameStyle", parent=styles["Title"], fontSize=22,
        textColor=colors.white if theme["header_bg"] else accent,
        spaceAfter=2, alignment=theme["name_align"],
    )
    contact_style = ParagraphStyle(
        "ContactStyle", parent=styles["Normal"], fontSize=9.5,
        textColor=colors.HexColor("#E5E7EB") if theme["header_bg"] else colors.HexColor("#555555"),
        spaceAfter=10, alignment=theme["name_align"],
    )
    section_style = ParagraphStyle(
        "SectionStyle", parent=styles["Heading2"], fontSize=12,
        textColor=accent, spaceBefore=12, spaceAfter=4,
    )
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10, leading=14)
    item_title_style = ParagraphStyle(
        "ItemTitle", parent=styles["Normal"], fontSize=10.5, leading=14, fontName="Helvetica-Bold",
    )

    story = []

    full_name = data.get("full_name", "")
    contact_bits = [data.get("email", ""), data.get("phone", ""), data.get("address", "")]
    link_bits = [b for b in [data.get("linkedin", ""), data.get("github", ""), data.get("portfolio", "")] if b]
    contact_line = " | ".join(filter(None, contact_bits))
    link_line = " | ".join(link_bits)

    if theme["header_bg"]:
        # Executive: dark header block spanning the page width
        header_table = Table(
            [[Paragraph(full_name, name_style)],
             [Paragraph(contact_line, contact_style)]] +
            ([[Paragraph(link_line, contact_style)]] if link_line else []),
            colWidths=[doc.width],
        )
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(theme["header_bg"])),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ("LEFTPADDING", (0, 0), (-1, -1), 18),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 10))
    else:
        story.append(Paragraph(full_name, name_style))
        story.append(Paragraph(contact_line, contact_style))
        if link_line:
            story.append(Paragraph(link_line, contact_style))
        bar_thickness = 2.2 if theme is TEMPLATES.get("modern") else 1.2
        story.append(HRFlowable(width="100%", color=accent, thickness=bar_thickness))

    if data.get("summary"):
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        story.append(Paragraph(data["summary"], body_style))

    if data.get("skills"):
        story.append(Paragraph("SKILLS", section_style))
        skills = [s.strip() for s in data["skills"].split(",") if s.strip()]
        story.append(Paragraph(" &nbsp;•&nbsp; ".join(skills), body_style))

    education = _safe_json(data.get("education"))
    if education:
        story.append(Paragraph("EDUCATION", section_style))
        for edu in education:
            story.append(Paragraph(f"{edu.get('degree','')} — {edu.get('institution','')}", item_title_style))
            story.append(Paragraph(f"{edu.get('year','')} &nbsp;|&nbsp; {edu.get('score','')}", body_style))
            story.append(Spacer(1, 4))

    experience = _safe_json(data.get("experience"))
    if experience:
        story.append(Paragraph("EXPERIENCE", section_style))
        for exp in experience:
            story.append(Paragraph(f"{exp.get('role','')} — {exp.get('company','')}", item_title_style))
            story.append(Paragraph(exp.get("duration", ""), body_style))
            if exp.get("description"):
                story.append(Paragraph(exp["description"], body_style))
            story.append(Spacer(1, 4))

    projects = _safe_json(data.get("projects"))
    if projects:
        story.append(Paragraph("PROJECTS", section_style))
        for proj in projects:
            story.append(Paragraph(proj.get("title", ""), item_title_style))
            if proj.get("description"):
                story.append(Paragraph(proj["description"], body_style))
            story.append(Spacer(1, 4))

    if data.get("achievements"):
        story.append(Paragraph("ACHIEVEMENTS", section_style))
        story.append(Paragraph(data["achievements"], body_style))

    if data.get("certifications"):
        story.append(Paragraph("CERTIFICATIONS", section_style))
        story.append(Paragraph(data["certifications"], body_style))

    if data.get("languages"):
        story.append(Paragraph("LANGUAGES", section_style))
        story.append(Paragraph(data["languages"], body_style))

    doc.build(story)
    return output_path


def _safe_json(value):
    if not value:
        return []
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return []
