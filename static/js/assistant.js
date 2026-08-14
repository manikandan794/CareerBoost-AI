/* ============================================================
   CareerBoost AI — floating assistant widget
   ============================================================ */

(function () {
  const ENDPOINT_TO_PAGE = {
    "resume.builder": "resume-builder",
    "resume.analyzer": "resume-analyzer",
    "coding.index": "coding-practice",
    "coding.problem_detail": "coding-practice",
    "interview.index": "interview-questions",
    "quiz.categories": "quiz",
    "quiz.take_quiz": "quiz",
    "dashboard.index": "dashboard",
    "companies.index": "companies",
    "ai_coach.hub": "ai-hub",
    "ai_coach.roadmap_page": "ai-roadmap",
    "ai_coach.skill_gap_page": "ai-skill-gap",
    "ai_coach.study_page": "ai-study",
    "ai_coach.quiz_generator_page": "ai-quiz-generator",
    "ai_coach.resume_match_page": "ai-resume-match",
    "ai_coach.company_prep_page": "ai-company-prep",
    "ai_coach.interview_coach_page": "ai-interview-coach",
    "gd.home": "group-discussion",
    "gd.topics": "group-discussion",
    "gd.session_page": "group-discussion",
  };

  const SUGGESTIONS_BY_PAGE = {
    "resume-builder": ["Help me write my summary", "How do I describe a project?", "Which template should I pick?"],
    "resume-analyzer": ["Why is my score low?", "What are missing keywords?", "Suggest stronger action verbs"],
    "coding-practice": ["Give me a hint", "Explain time complexity", "My tests are failing, why?"],
    "interview-questions": ["I'm nervous, help", "Explain the STAR method", "Tips for Python questions"],
    "quiz": ["Quantitative tips", "Logical reasoning tricks", "Verbal ability tips"],
    "dashboard": ["What should I practice next?", "How do I improve my score?"],
    "companies": ["Which companies suit a fresher?", "What is TCS eligibility?"],
    "ai-hub": ["Create my career roadmap", "Analyze my skill gap", "Start a mock interview"],
    "ai-roadmap": ["What should I include as current skills?", "How long should my roadmap be?"],
    "ai-skill-gap": ["What counts as a beginner skill?", "How is readiness calculated?"],
    "ai-study": ["Explain this topic simply", "Generate flashcards for this", "Give me a revision plan"],
    "ai-quiz-generator": ["Make it harder", "Focus on a narrower topic"],
    "ai-resume-match": ["What's a good match score?", "How do I fix missing keywords?"],
    "ai-company-prep": ["What should I focus on first?", "How do I use the 7-day plan?"],
    "ai-interview-coach": ["How is my answer scored?", "Tips before I start"],
    "group-discussion": ["Practice Group Discussion", "Tips for GD confidence", "How is my GD scored?"],
    "general": ["What can you do?", "Help me get started"],
  };

  function currentPage() {
    const endpoint = document.body.getAttribute("data-endpoint") || "";
    return ENDPOINT_TO_PAGE[endpoint] || "general";
  }

  function currentContext() {
    // Coding problem pages expose PROBLEM_TITLE / PROBLEM_LANGUAGE globals for richer context.
    if (typeof window.PROBLEM_TITLE !== "undefined") {
      const ctx = { problem_title: window.PROBLEM_TITLE };
      if (typeof window.PROBLEM_LANGUAGE !== "undefined") {
        ctx.problem_language = window.PROBLEM_LANGUAGE;
      }
      return ctx;
    }
    return {};
  }

  const state = {
    open: false,
    history: [], // [{role, content}]
  };

  function el(id) { return document.getElementById(id); }

  function addMessage(role, text) {
    const wrap = el("cbAssistantMessages");
    const bubble = document.createElement("div");
    bubble.className = "cb-msg cb-msg-" + role;
    bubble.textContent = text;
    wrap.appendChild(bubble);
    wrap.scrollTop = wrap.scrollHeight;
    state.history.push({ role, content: text });
  }

  function addTyping() {
    const wrap = el("cbAssistantMessages");
    const bubble = document.createElement("div");
    bubble.className = "cb-msg cb-msg-assistant cb-msg-typing";
    bubble.id = "cbTypingBubble";
    bubble.innerHTML = "<span></span><span></span><span></span>";
    wrap.appendChild(bubble);
    wrap.scrollTop = wrap.scrollHeight;
  }

  function removeTyping() {
    const bubble = el("cbTypingBubble");
    if (bubble) bubble.remove();
  }

  function renderSuggestions() {
    const box = el("cbAssistantSuggestions");
    box.innerHTML = "";
    const page = currentPage();
    const suggestions = SUGGESTIONS_BY_PAGE[page] || SUGGESTIONS_BY_PAGE.general;
    suggestions.forEach((text) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "cb-suggestion-chip";
      chip.textContent = text;
      chip.addEventListener("click", () => sendMessage(text));
      box.appendChild(chip);
    });
  }

  function sendMessage(text) {
    text = (text || el("cbAssistantInput").value || "").trim();
    if (!text) return;
    el("cbAssistantInput").value = "";
    addMessage("user", text);
    addTyping();

    fetch("/api/assistant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        page: currentPage(),
        context: currentContext(),
        history: state.history.slice(0, -1).slice(-8),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        removeTyping();
        addMessage("assistant", data.reply || "Sorry, I didn't catch that.");
      })
      .catch(() => {
        removeTyping();
        addMessage("assistant", "Something went wrong reaching the assistant. Please try again.");
      });
  }

  function openPanel() {
    state.open = true;
    el("cbAssistant").classList.add("cb-open");
    if (!el("cbAssistantMessages").childElementCount) {
      addMessage("assistant", "Hi! I'm your CareerBoost AI Assistant. Ask me anything about this page, or tap a suggestion below.");
    }
    renderSuggestions();
    el("cbAssistantInput").focus();
  }

  function closePanel() {
    state.open = false;
    el("cbAssistant").classList.remove("cb-open");
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!el("cbAssistant")) return;

    el("cbAssistantToggle").addEventListener("click", () => {
      state.open ? closePanel() : openPanel();
    });
    el("cbAssistantClose").addEventListener("click", closePanel);
    el("cbAssistantForm").addEventListener("submit", (e) => {
      e.preventDefault();
      sendMessage();
    });

    // Public API used by other pages (e.g. "Ask AI" button on coding problems)
    window.CareerBoostAssistant = {
      open: openPanel,
      ask: (text) => { if (!state.open) openPanel(); sendMessage(text); },
    };
  });
})();
