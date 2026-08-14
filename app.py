"""
CareerBoost AI — Flask application entry point.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

import os
from flask import Flask

# Load variables from a local .env file (if present) into the process
# environment before anything reads them. Harmless in production, where
# real secrets are injected by the platform and no .env file exists.
from dotenv import load_dotenv
load_dotenv()

from config import Config
from models.db import close_db, init_db

# Blueprints (each file owns one feature area — keeps routing organized)
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp
from routes.dashboard import bp as dashboard_bp
from routes.resume import bp as resume_bp
from routes.quiz import bp as quiz_bp
from routes.interview import bp as interview_bp
from routes.coding import bp as coding_bp
from routes.companies import bp as companies_bp
from routes.profile import bp as profile_bp
from routes.admin import bp as admin_bp
from routes.assistant import bp as assistant_bp
from routes.ai_coach import bp as ai_coach_bp
from routes.gd import bp as gd_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Make sure the database directory exists before first connection.
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)
    os.makedirs(app.config["RESUME_EXPORT_DIR"], exist_ok=True)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(ai_coach_bp)
    app.register_blueprint(gd_bp)

    # Close DB connection at the end of each request
    app.teardown_appcontext(close_db)

    # Make current year & session data available in every template
    @app.context_processor
    def inject_globals():
        from flask import session
        return {"current_year": __import__("datetime").datetime.now().year,
                 "logged_in": "user_id" in session}

    # Friendly error pages
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template("errors/403.html"), 403

    with app.app_context():
        init_db(app)

    return app


app = create_app()

if __name__ == "__main__":
    # Local dev default: python app.py -> http://127.0.0.1:5000
    # Cloud platforms provide PORT and expect the app to bind 0.0.0.0.
    # DEBUG is env-controlled and defaults to off, so a forgotten env var
    # can never accidentally leave the Werkzeug debugger open in production.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
