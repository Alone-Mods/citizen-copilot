from flask import Blueprint, jsonify
from database.db import get_connection
from config import Config

# Create the health Blueprint
health_bp = Blueprint("health", __name__)

@health_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    Diagnostic endpoint that checks backend status and database connectivity.
    """
    try:
        # Establish a test connection to the database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute query to verify tables are present
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Exclude sqlite_sequence auto-created table from diagnostic log list
        filtered_tables = [t for t in tables if t != "sqlite_sequence"]
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "tables_found": len(filtered_tables),
            "tables": filtered_tables,
            "debug_mode": Config.DEBUG
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500
