from flask import Blueprint, request, jsonify, session
from database.db import db_get_scheme_by_id, db_get_eligibility_history_by_user
from models.eligibility_history import EligibilityHistory

from services.eligibility_engine import evaluate_user_eligibility
from services.scheme_service import get_scheme_recommendations

# Create the ai Blueprint
ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/api/ai/eligibility", methods=["POST"])
def check_eligibility():
    """
    Evaluates user eligibility for a specific scheme using rule matchers and AI prompt services.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    data = request.get_json() or {}
    scheme_id = data.get("scheme_id")

    if not scheme_id:
        return jsonify({
            "status": "error",
            "message": "Field 'scheme_id' is required in JSON payload."
        }), 400

    try:
        # Check if the scheme exists
        scheme = db_get_scheme_by_id(scheme_id)
        if not scheme:
            return jsonify({
                "status": "error",
                "message": f"Scheme with ID {scheme_id} not found."
            }), 404

        # Delegate evaluation to eligibility service engine
        evaluation_result = evaluate_user_eligibility(user_id, scheme_id)
        
        return jsonify({
            "status": "success",
            "evaluation": evaluation_result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to evaluate eligibility: {str(e)}"
        }), 500

@ai_bp.route("/api/ai/recommend", methods=["POST"])
def get_recommendations():
    """
    Analyzes user profile variables and returns ranked opportunities matching them.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        # Delegate matching query logic to service
        recommendations = get_scheme_recommendations(user_id)
        
        return jsonify({
            "status": "success",
            "count": len(recommendations),
            "recommendations": recommendations
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to generate recommendations: {str(e)}"
        }), 500

@ai_bp.route("/api/ai/history", methods=["GET"])
def list_eligibility_history():
    """
    Returns user history records for all prior AI eligibility evaluations.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        raw_history = db_get_eligibility_history_by_user(user_id)
        serialized_history = []
        
        for row in raw_history:
            record = EligibilityHistory.from_dict(row)
            if record:
                serialized_history.append(record.to_dict())

        return jsonify({
            "status": "success",
            "count": len(serialized_history),
            "history": serialized_history
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve eligibility history: {str(e)}"
        }), 500
