/* ============================================================
   CareerBoost AI — Resume Builder wizard controller
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("resumeForm");
  if (!form) return;

  const TOTAL_STEPS = 7;
  let currentStep = 1;

  const pills = document.querySelectorAll(".resume-step-pill");
  const panels = document.querySelectorAll(".resume-step-panel");
  const prevBtn = document.getElementById("resumePrevBtn");
  const nextBtn = document.getElementById("resumeNextBtn");
  const submitBtn = document.getElementById("resumeSubmitBtn");

  function showStep(step) {
    currentStep = step;
    panels.forEach((p) => p.classList.toggle("active", Number(p.dataset.panel) === step));
    pills.forEach((pill) => {
      const n = Number(pill.dataset.step);
      pill.classList.toggle("active", n === step);
      pill.classList.toggle("done", n < step);
    });
    prevBtn.style.visibility = step === 1 ? "hidden" : "visible";
    nextBtn.style.display = step === TOTAL_STEPS ? "none" : "inline-flex";
    submitBtn.style.display = step === TOTAL_STEPS ? "inline-flex" : "none";
    window.scrollTo({ top: form.offsetTop - 100, behavior: "smooth" });
  }

  pills.forEach((pill) => {
    pill.addEventListener("click", () => showStep(Number(pill.dataset.step)));
  });
  nextBtn.addEventListener("click", () => {
    if (currentStep < TOTAL_STEPS) showStep(currentStep + 1);
  });
  prevBtn.addEventListener("click", () => {
    if (currentStep > 1) showStep(currentStep - 1);
  });

  // ---------- Template picker ----------
  const templateInput = document.getElementById("templateInput");
  document.querySelectorAll(".resume-template-option").forEach((opt) => {
    opt.addEventListener("click", () => {
      document.querySelectorAll(".resume-template-option").forEach((o) => o.classList.remove("selected"));
      opt.classList.add("selected");
      templateInput.value = opt.dataset.template;
    });
  });

  // ---------- Live preview ----------
  const preview = document.getElementById("resumeLivePreview");

  function esc(str) {
    const d = document.createElement("div");
    d.textContent = str || "";
    return d.innerHTML;
  }

  function updateSimpleFields() {
    const get = (name) => (form.querySelector(`[name="${name}"]`) || {}).value || "";

    preview.querySelector('[data-out="full_name"]').textContent = get("full_name") || "Your Name";
    const contactBits = [get("email"), get("phone"), get("address")].filter(Boolean);
    preview.querySelector('[data-out="contact"]').textContent = contactBits.length ? contactBits.join(" • ") : "email • phone • location";
    const linkBits = [get("linkedin"), get("github"), get("portfolio")].filter(Boolean);
    preview.querySelector('[data-out="links"]').textContent = linkBits.join(" • ");

    const singleFieldMap = {
      summary: get("summary"),
      skills: get("skills").split(",").map((s) => s.trim()).filter(Boolean).join("  •  "),
      certifications: get("certifications"),
      achievements: get("achievements"),
    };
    Object.entries(singleFieldMap).forEach(([key, val]) => {
      const section = preview.querySelector(`[data-section="${key}"]`);
      const out = preview.querySelector(`[data-out="${key}"]`);
      if (val && val.trim()) {
        section.style.display = "block";
        out.innerHTML = esc(val).replace(/\n/g, "<br>");
      } else {
        section.style.display = "none";
      }
    });
  }

  function collectRepeatGroup(groupName, fieldOrder) {
    const container = groupName === "education" ? "edu-container" : groupName === "experience" ? "exp-container" : "proj-container";
    const blocks = document.getElementById(container).querySelectorAll(".repeatable-block");
    const rows = [];
    blocks.forEach((block) => {
      const values = fieldOrder.map((name) => (block.querySelector(`[name="${name}"]`) || {}).value || "");
      if (values.some((v) => v.trim())) rows.push(values);
    });
    return rows;
  }

  function updateRepeatSections() {
    const eduRows = collectRepeatGroup("education", ["edu_degree", "edu_institution", "edu_year", "edu_score"]);
    const eduSection = preview.querySelector('[data-section="education"]');
    const eduOut = preview.querySelector('[data-out="education"]');
    if (eduRows.length) {
      eduSection.style.display = "block";
      eduOut.innerHTML = eduRows.map(([deg, inst, year, score]) =>
        `<div style="margin-bottom:6px;"><strong>${esc(deg)}</strong>${inst ? " — " + esc(inst) : ""}<br><span style="color:#666;">${esc(year)} ${score ? "| " + esc(score) : ""}</span></div>`
      ).join("");
    } else { eduSection.style.display = "none"; }

    const expRows = collectRepeatGroup("experience", ["exp_role", "exp_company", "exp_duration", "exp_description"]);
    const expSection = preview.querySelector('[data-section="experience"]');
    const expOut = preview.querySelector('[data-out="experience"]');
    if (expRows.length) {
      expSection.style.display = "block";
      expOut.innerHTML = expRows.map(([role, company, duration, desc]) =>
        `<div style="margin-bottom:6px;"><strong>${esc(role)}</strong>${company ? " — " + esc(company) : ""}<br><span style="color:#666;">${esc(duration)}</span>${desc ? "<br>" + esc(desc) : ""}</div>`
      ).join("");
    } else { expSection.style.display = "none"; }

    const projRows = collectRepeatGroup("projects", ["proj_title", "proj_description"]);
    const projSection = preview.querySelector('[data-section="projects"]');
    const projOut = preview.querySelector('[data-out="projects"]');
    if (projRows.length) {
      projSection.style.display = "block";
      projOut.innerHTML = projRows.map(([title, desc]) =>
        `<div style="margin-bottom:6px;"><strong>${esc(title)}</strong>${desc ? "<br>" + esc(desc) : ""}</div>`
      ).join("");
    } else { projSection.style.display = "none"; }
  }

  function refreshPreview() {
    updateSimpleFields();
    updateRepeatSections();
  }

  form.addEventListener("input", refreshPreview);
  // New repeatable blocks are added dynamically — listen at the document level for clicks that add blocks.
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-add-block]") || e.target.closest(".remove-block-btn")) {
      setTimeout(refreshPreview, 0);
    }
  });

  showStep(1);
  refreshPreview();
});
