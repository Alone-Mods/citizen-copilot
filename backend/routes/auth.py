import re
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from database.db import db_create_user, db_get_user_by_email, db_get_user_by_id
from models.user import User

# Create the auth Blueprint
auth_bp = Blueprint("auth", __name__)

def is_valid_email(email):
    """Simple email validation check."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """
    Registers a new user profile, validating input fields and hashing passwords.
    """
    data = request.get_json() or {}
    
    # Required registration fields
    required_fields = ["full_name", "email", "password", "state", "district"]
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            return jsonify({
                "status": "error",
                "message": f"Field '{field}' is required and cannot be empty."
            }), 400

    full_name = data.get("full_name").strip()
    email = data.get("email").strip().lower()
    password = data.get("password")
    
    if not is_valid_email(email):
        return jsonify({
            "status": "error",
            "message": "Invalid email address format."
        }), 400

    # Ensure email is unique
    existing_user = db_get_user_by_email(email)
    if existing_user:
        return jsonify({
            "status": "error",
            "message": "An account with this email address already exists."
        }), 409

    # Generate password hash
    password_hash = generate_password_hash(password)

    # Optional fields with logical defaults
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
        # Create user record in database
        new_user_id = db_create_user(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
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
        
        return jsonify({
            "status": "success",
            "message": "User registered successfully.",
            "user_id": new_user_id
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database insertion error: {str(e)}"
        }), 500

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Authenticates user credentials and initiates a secure session.
    """
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required fields."
        }), 400

    user_data = db_get_user_by_email(email)
    if not user_data:
        return jsonify({
            "status": "error",
            "message": "Invalid email or password."
        }), 401

    # Map raw user record dictionary to User domain model object
    user = User.from_dict(user_data)
    
    # Check credentials
    if not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "Invalid email or password."
        }), 401

    # Set session value
    session["user_id"] = user.user_id

    return jsonify({
        "status": "success",
        "message": "Logged in successfully.",
        "user": user.to_dict(exclude_password=True)
    }), 200

@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """
    Clears the logged-in user session.
    """
    session.pop("user_id", None)
    return jsonify({
        "status": "success",
        "message": "Logged out successfully."
    }), 200

@auth_bp.route("/api/auth/session", methods=["GET"])
def check_session():
    """
    Verifies active user session and returns current profile data.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    user_data = db_get_user_by_id(user_id)
    if not user_data:
        # Session user_id doesn't match any db record
        session.pop("user_id", None)
        return jsonify({
            "status": "error",
            "message": "Unauthorized. User session is invalid."
        }), 401

    user = User.from_dict(user_data)
    return jsonify({
        "status": "success",
        "user": user.to_dict(exclude_password=True)
    }), 200
