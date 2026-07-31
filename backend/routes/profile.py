from flask import Blueprint, request, jsonify, session
from database.db import db_get_user_by_id, db_update_user
from models.user import User

# Create the profile Blueprint
profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/api/profile", methods=["GET"])
def get_profile():
    """
    Retrieves the logged-in user's profile metadata.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    user_data = db_get_user_by_id(user_id)
    if not user_data:
        session.pop("user_id", None)
        return jsonify({
            "status": "error",
            "message": "Unauthorized. Profile not found."
        }), 401

    user = User.from_dict(user_data)
    return jsonify({
        "status": "success",
        "user": user.to_dict(exclude_password=True)
    }), 200

@profile_bp.route("/api/profile", methods=["PUT"])
def update_profile():
    """
    Updates the logged-in user's profile metadata, enforcing validation limits.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    # Verify user exists before updating
    user_data = db_get_user_by_id(user_id)
    if not user_data:
        session.pop("user_id", None)
        return jsonify({
            "status": "error",
            "message": "Unauthorized. Profile not found."
        }), 401

    data = request.get_json() or {}

    # Required fields validation
    required_fields = ["full_name", "state", "district"]
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            return jsonify({
                "status": "error",
                "message": f"Field '{field}' is required and cannot be empty."
            }), 400

    full_name = data.get("full_name").strip()
    phone_number = data.get("phone_number", "").strip() or None

    try:
        age = int(data.get("age")) if data.get("age") is not None else None
        if age is not None and (age < 0 or age > 120):
            return jsonify({"status": "error", "message": "Age must be between 0 and 120."}), 400
    except ValueError:
        return jsonify({"status": "error", "message": "Age must be a valid integer."}), 400

    gender = data.get("gender")
    valid_genders = ["Male", "Female", "Non-Binary", "Other", "Prefer Not to Say"]
    if gender and gender not in valid_genders:
        return jsonify({
            "status": "error",
            "message": f"Gender must be one of: {', '.join(valid_genders)}."
        }), 400

    state = data.get("state").strip()
    district = data.get("district").strip()
    education = data.get("education", "").strip() or None
    occupation = data.get("occupation", "").strip() or None

    try:
        annual_family_income = float(data.get("annual_family_income")) if data.get("annual_family_income") is not None else 0.0
        if annual_family_income < 0:
            return jsonify({"status": "error", "message": "Annual family income must be non-negative."}), 400
    except ValueError:
        return jsonify({"status": "error", "message": "Annual family income must be a valid number."}), 400

    category = data.get("category")
    valid_categories = ["General", "OBC", "SC", "ST", "EWS"]
    if category and category not in valid_categories:
        return jsonify({
            "status": "error",
            "message": f"Category must be one of: {', '.join(valid_categories)}."
        }), 400

    is_disabled = 1 if data.get("is_disabled") in [1, True, "1", "true"] else 0

    try:
        # Perform db update query
        db_update_user(
            user_id=user_id,
            full_name=full_name,
            phone_number=phone_number,
            age=age,
            gender=gender,
            state=state,
            district=district,
            education=education,
            occupation=occupation,
            annual_family_income=annual_family_income,
            category=category,
            is_disabled=is_disabled
        )
        
        # Fetch updated user profile
        updated_data = db_get_user_by_id(user_id)
        user = User.from_dict(updated_data)
        
        return jsonify({
            "status": "success",
            "message": "Profile updated successfully.",
            "user": user.to_dict(exclude_password=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database update error: {str(e)}"
        }), 500
