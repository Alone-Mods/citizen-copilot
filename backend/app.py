import sys
import os

# Ensure backend root directory is on Python system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import init_database

# Import all 7 Blueprints
from routes.health import health_bp
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.schemes import schemes_bp
from routes.documents import documents_bp
from routes.notifications import notifications_bp
from routes.ai import ai_bp

# Import background task scheduler
from services.scheduler import start_scheduler

def create_app():
    """
    Application factory function configuring Flask, CORS, database, Blueprints,
    and background schedulers.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for cross-origin frontend requests
    CORS(app, supports_credentials=True)

    # Initialize database tables
    with app.app_context():
        init_database()

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(ai_bp)

    # Start background deadline scheduler thread
    try:
        start_scheduler(interval_seconds=3600)
    except Exception as e:
        app.logger.warning(f"Failed to start task scheduler: {str(e)}")

    # Register global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found on the server."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected server error occurred."}), 500

    return app

# Instantiate Flask application
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
