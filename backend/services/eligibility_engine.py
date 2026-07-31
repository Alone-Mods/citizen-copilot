import json
from database.db import (
    db_get_user_by_id,
    db_get_scheme_by_id,
    db_create_eligibility_history,
    db_create_notification
)
from services.gemini_service import analyze_eligibility
from services.document_checker import check_uploaded_documents

def evaluate_user_eligibility(user_id, scheme_id):
    """
    Evaluates eligibility between a user profile and a scheme, logging output to database history
    and creating a notification alert.
    
    Args:
        user_id (int): ID of the user.
        scheme_id (int): ID of the target scheme.
        
    Returns:
        dict: Complete evaluation payload.
    """
    # Fetch user profile
    user = db_get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    # Fetch scheme details
    scheme = db_get_scheme_by_id(scheme_id)
    if not scheme:
        raise ValueError(f"Scheme with ID {scheme_id} not found.")

    # Check document completeness
    doc_check = check_uploaded_documents(user_id, scheme.get("required_documents"))

    # Perform Gemini AI / Fallback analysis
    ai_result = analyze_eligibility(user, scheme)

    eligible = ai_result.get("eligible", False)
    match_percentage = ai_result.get("match_percentage", 0.0)
    ai_explanation = ai_result.get("ai_explanation", "")
    missing_requirements = ai_result.get("missing_requirements", [])
    missing_documents = doc_check.get("missing_documents", [])

    # Format result status string
    eligibility_result_str = "Eligible" if eligible else "Ineligible"

    # Serialize missing_requirements to JSON string for SQLite storage
    missing_reqs_json = json.dumps({
        "criteria": missing_requirements,
        "documents": missing_documents
    })

    # Log evaluation result in eligibility_history table
    history_id = db_create_eligibility_history(
        user_id=user_id,
        scheme_id=scheme_id,
        eligibility_result=eligibility_result_str,
        match_percentage=match_percentage,
        ai_explanation=ai_explanation,
        missing_requirements=missing_reqs_json
    )

    # Dispatch notification alert to user
    scheme_title = scheme.get("title", "Government Scheme")
    notif_title = f"Eligibility Check: {scheme_title}"
    if eligible:
        notif_msg = f"Good news! You qualify for {scheme_title} with a match score of {match_percentage:.0f}%."
        notif_type = "Success"
    else:
        notif_msg = f"You checked eligibility for {scheme_title}. Click to review missing requirements."
        notif_type = "Info"

    try:
        db_create_notification(user_id, notif_title, notif_msg, notif_type)
    except Exception as e:
        print(f"Warning: Failed to create notification log: {str(e)}")

    return {
        "history_id": history_id,
        "user_id": user_id,
        "scheme_id": scheme_id,
        "scheme_title": scheme_title,
        "eligible": eligible,
        "match_percentage": match_percentage,
        "ai_explanation": ai_explanation,
        "missing_requirements": missing_requirements,
        "missing_documents": missing_documents,
        "has_all_documents": doc_check.get("has_all_documents", False)
    }
