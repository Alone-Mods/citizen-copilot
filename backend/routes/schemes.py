from flask import Blueprint, request, jsonify
from database.db import db_get_all_schemes, db_get_scheme_by_id, db_search_schemes
from models.scheme import Scheme

# Create the schemes Blueprint
schemes_bp = Blueprint("schemes", __name__)

@schemes_bp.route("/api/schemes", methods=["GET"])
def get_all_schemes():
    """
    Returns all government schemes available in the platform.
    """
    try:
        raw_schemes = db_get_all_schemes()
        serialized_schemes = []
        
        for row in raw_schemes:
            scheme = Scheme.from_dict(row)
            if scheme:
                serialized_schemes.append(scheme.to_dict())
                
        return jsonify({
            "status": "success",
            "count": len(serialized_schemes),
            "schemes": serialized_schemes
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve schemes: {str(e)}"
        }), 500

@schemes_bp.route("/api/schemes/<int:scheme_id>", methods=["GET"])
def get_scheme_by_id(scheme_id):
    """
    Returns details of a single government scheme by its ID.
    """
    try:
        raw_scheme = db_get_scheme_by_id(scheme_id)
        if not raw_scheme:
            return jsonify({
                "status": "error",
                "message": f"Scheme with ID {scheme_id} not found."
            }), 404
            
        scheme = Scheme.from_dict(raw_scheme)
        return jsonify({
            "status": "success",
            "scheme": scheme.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve scheme details: {str(e)}"
        }), 500

@schemes_bp.route("/api/schemes/search", methods=["GET"])
def search_schemes():
    """
    Searches schemes based on keywords (title/description) and category criteria.
    """
    # Extract query params
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    
    # If parameters are empty, fallback to returning all schemes
    if not query and not category:
        return get_all_schemes()
        
    try:
        raw_schemes = db_search_schemes(
            query_term=query if query else None,
            category_term=category if category else None
        )
        
        serialized_schemes = []
        for row in raw_schemes:
            scheme = Scheme.from_dict(row)
            if scheme:
                serialized_schemes.append(scheme.to_dict())
                
        return jsonify({
            "status": "success",
            "query": query or None,
            "category": category or None,
            "count": len(serialized_schemes),
            "schemes": serialized_schemes
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to perform search: {str(e)}"
        }), 500
