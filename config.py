"""
Central configuration for the CareerBoost AI Flask application.
Keeping config in one place makes it easy to switch between
development / production settings later.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ConfigurationError(RuntimeError):
    """Raised when a required environment variable is missing at startup."""


def _require_env(var_name: str) -> str:
    """Read a required environment variable or fail loudly and clearly.

    There is intentionally NO hardcoded fallback for security-sensitive
    values (secret key, admin credentials). Copy `.env.example` to `.env`
    and fill in real values, or set these in your platform's environment
    variable settings before starting the app.
    """
    value = os.environ.get(var_name)
    if not value:
        raise ConfigurationError(
            f"Missing required environment variable: {var_name}\n"
            f"Set it in your .env file (copy .env.example to .env and fill "
            f"it in) or in your hosting platform's environment variable "
            f"settings before starting the app. Refusing to start with a "
            f"default/insecure value."
        )
    return value


class Config:
    # Secret key used to sign session cookies. MUST be provided via an
    # environment variable — there is no insecure default.
    SECRET_KEY = _require_env("SECRET_KEY")

    # SQLite database file lives inside the /database folder.
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "careerboost.db")

    # Where generated resume PDFs are temporarily written before download.
    RESUME_EXPORT_DIR = os.path.join(BASE_DIR, "static", "generated")

    # Default admin account created automatically on first run.
    # MUST be provided via environment variables — there is no
    # hardcoded/default admin email or password.
    DEFAULT_ADMIN_EMAIL = _require_env("DEFAULT_ADMIN_EMAIL")
    DEFAULT_ADMIN_PASSWORD = _require_env("DEFAULT_ADMIN_PASSWORD")

    # ---- Face Unlock (optional, opt-in) -----------------------------
    # Face descriptors are 128-d vectors produced client-side by
    # face-api.js. Lower distance = more similar; face-api.js's own docs
    # suggest ~0.6 as a typical match threshold for its embeddings.
    # This is a convenience login layer, NOT a hardened biometric
    # security system — see routes/auth.py for caveats.
    FACE_MATCH_THRESHOLD = 0.55
    FACE_MAX_ATTEMPTS = 5          # per email, per window, before a cooldown
    FACE_ATTEMPT_WINDOW_SECONDS = 5 * 60
