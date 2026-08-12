"""Clearcut — a small Flask app serving three image tools and a blog.

Run it with:  python app.py
Then open:    http://127.0.0.1:5000
"""
from flask import Flask, render_template, jsonify, request

from config import Config, BRAND_NAME, BRAND_TAGLINE, MAX_UPLOAD_MB
from routes.main import main
from routes.tools import tools
from utils.cleanup import start_cleanup_thread


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register the two groups of routes.
    app.register_blueprint(main)
    app.register_blueprint(tools)

    # Make brand info available to every template without passing it each time.
    @app.context_processor
    def inject_globals():
        return {
            "BRAND_NAME": BRAND_NAME,
            "BRAND_TAGLINE": BRAND_TAGLINE,
            "MAX_UPLOAD_MB": MAX_UPLOAD_MB,
        }

    # ---- Global error handlers ---------------------------------------------
    def wants_json():
        # API calls (fetch) and /api paths should get JSON, not an HTML page.
        return request.path.startswith("/api") or "application/json" in (
            request.headers.get("Accept", "")
        )

    @app.errorhandler(413)
    def too_large(_e):
        msg = f"That file is too big. The limit is {MAX_UPLOAD_MB} MB."
        if wants_json():
            return jsonify(error=msg), 413
        return render_template("error.html", code=413, message=msg), 413

    @app.errorhandler(404)
    def not_found(_e):
        if wants_json():
            return jsonify(error="Not found."), 404
        return render_template(
            "error.html", code=404, message="We couldn't find that page."
        ), 404

    @app.errorhandler(500)
    def server_error(_e):
        if wants_json():
            return jsonify(error="Something went wrong on our end."), 500
        return render_template(
            "error.html", code=500, message="Something went wrong on our end."
        ), 500

    # Start the temp-folder cleanup sweeper (no-op in normal use, safety net).
    start_cleanup_thread()

    return app


app = create_app()

if __name__ == "__main__":
    # debug=True gives helpful error pages while you're learning.
    # Turn it off (debug=False) before putting this on a real server.
    app.run(host="127.0.0.1", port=5000, debug=True)
