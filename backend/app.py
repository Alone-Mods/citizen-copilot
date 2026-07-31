from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, supports_credentials=True)

    # Base route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "status": "success",
            "message": "Citizen Copilot Backend API is running",
            "version": "1.0.0"
        })

    # Health check endpoint to verify database connectivity
    @app.route("/api/health", methods=["GET"])
    def health_check():
        try:
            # Connect to database via absolute path from configuration
            conn = sqlite3.connect(app.config["DATABASE_PATH"])
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "tables_found": len(tables),
                "debug_mode": app.config["DEBUG"]
            })
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
