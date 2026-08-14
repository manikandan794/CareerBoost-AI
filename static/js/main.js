/* ============================================================
   CareerBoost AI — shared front-end behaviour
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

  // Auto-dismiss flash alerts after 4s
  document.querySelectorAll(".alert-auto-dismiss").forEach((el) => {
    setTimeout(() => {
      el.classList.remove("show");
      el.classList.add("fade");
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // Navbar shadow on scroll
  const nav = document.querySelector(".navbar-cb");
  if (nav) {
    window.addEventListener("scroll", () => {
      nav.style.boxShadow = window.scrollY > 10 ? "0 2px 12px rgba(0,0,0,0.08)" : "none";
    });
  }

  // Reveal-on-scroll for elements with .reveal-on-scroll
  const revealEls = document.querySelectorAll(".reveal-on-scroll");
  if (revealEls.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-fade-up");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach((el) => observer.observe(el));
  }

  initResumeBuilder();
  initQuizTimer();
  initPasswordToggle();
  initNewsletterForm();
});

/* ---------- Resume builder: add/remove repeatable blocks ---------- */
function initResumeBuilder() {
  document.querySelectorAll("[data-add-block]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const templateId = btn.getAttribute("data-add-block");
      const container = document.getElementById(templateId + "-container");
      const template = document.getElementById(templateId + "-template");
      if (!container || !template) return;
      const clone = template.content.cloneNode(true);
      container.appendChild(clone);
    });
  });

  document.addEventListener("click", (e) => {
    if (e.target.closest(".remove-block-btn")) {
      const block = e.target.closest(".repeatable-block");
      if (block) block.remove();
    }
  });
}

/* ---------- Quiz countdown timer ---------- */
function initQuizTimer() {
  const timerEl = document.getElementById("quizTimer");
  const form = document.getElementById("quizForm");
  if (!timerEl || !form) return;

  let seconds = 10 * 60; // 10 minutes
  const interval = setInterval(() => {
    seconds--;
    const m = Math.floor(seconds / 60).toString().padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    timerEl.textContent = `${m}:${s}`;
    if (seconds <= 60) timerEl.classList.add("text-danger");
    if (seconds <= 0) {
      clearInterval(interval);
      form.submit();
    }
  }, 1000);
}

/* ---------- Footer newsletter subscribe button ---------- */
function initNewsletterForm() {
  const btn = document.getElementById("newsletter-btn");
  const input = document.getElementById("newsletter-email");
  const msg = document.getElementById("newsletter-msg");
  if (!btn || !input || !msg) return;

  function showMessage(text, ok) {
    msg.textContent = text;
    msg.className = "d-block mt-2 " + (ok ? "text-success" : "text-danger");
  }

  function submitEmail() {
    const email = input.value.trim();
    if (!email) {
      showMessage("Please enter an email address.", false);
      return;
    }

    btn.disabled = true;
    fetch("/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email }),
    })
      .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
      .then(({ ok, data }) => {
        showMessage(data.message, ok);
        if (ok) input.value = "";
      })
      .catch(() => showMessage("Something went wrong. Please try again.", false))
      .finally(() => {
        btn.disabled = false;
      });
  }

  btn.addEventListener("click", submitEmail);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      submitEmail();
    }
  });
}

/* ---------- Show/hide password fields ---------- */
function initPasswordToggle() {
  document.querySelectorAll(".toggle-password").forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = document.querySelector(btn.getAttribute("data-target"));
      if (!input) return;
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      btn.querySelector("i").className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
    });
  });
}
