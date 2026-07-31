from database.db import db_get_user_by_id, db_get_all_schemes
from models.scheme import Scheme

def get_scheme_recommendations(user_id):
    """
    Analyzes a citizen's profile and returns a sorted list of recommended schemes
    ranked by eligibility match score.
    
    Args:
        user_id (int): ID of the user.
        
    Returns:
        list: Ranked scheme dictionaries with attached match percentage and recommendation notes.
    """
    user = db_get_user_by_id(user_id)
    if not user:
        return []

    raw_schemes = db_get_all_schemes()
    ranked_schemes = []

    user_income = user.get("annual_family_income", 0) or 0
    user_category = user.get("category", "General")
    user_gender = user.get("gender", "")
    user_occupation = (user.get("occupation") or "").lower()

    for row in raw_schemes:
        scheme_obj = Scheme.from_dict(row)
        if not scheme_obj:
            continue

        scheme_dict = scheme_obj.to_dict()
        title = scheme_dict.get("title", "")
        category_name = scheme_dict.get("category", "")

        match_score = 70.0  # Base match score for available opportunities
        reasons = []

        # 1. Occupation/Domain alignment
        if "farmer" in user_occupation and category_name == "Agriculture":
            match_score += 25.0
            reasons.append("Matches your occupation as a farmer.")
        elif "student" in user_occupation and category_name == "Education":
            match_score += 25.0
            reasons.append("Matches your student status.")

        # 2. SC/ST Category alignment for post-matric scholarships
        if "SC Students" in title:
            if user_category == "SC":
                match_score += 10.0
                reasons.append("Matches your SC category eligibility.")
            else:
                match_score -= 50.0

        # 3. Income alignment
        if "Scholarship" in title and user_income > 250000:
            match_score -= 40.0
        elif "Awas Yojana" in title and user_income <= 300000:
            match_score += 15.0
            reasons.append("Matches your family income bracket.")

        # 4. Gender alignment
        if "Lakhpati Didi" in title or category_name == "Women Empowerment":
            if user_gender == "Female":
                match_score += 20.0
                reasons.append("Tailored for female citizens.")
            else:
                match_score -= 60.0

        # Bound score between 10% and 100%
        final_score = max(10.0, min(100.0, match_score))
        
        scheme_dict["match_percentage"] = final_score
        scheme_dict["recommendation_reason"] = " ".join(reasons) if reasons else "General opportunity fitting your region."

        ranked_schemes.append(scheme_dict)

    # Sort schemes by match_percentage descending
    ranked_schemes.sort(key=lambda s: s["match_percentage"], reverse=True)
    return ranked_schemes
