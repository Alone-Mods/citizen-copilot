import os
import sys
import json

# =====================================================================
# PYTHON 3.14 COMPATIBILITY WORKAROUND FOR PROTOBUF
# Prevents crash: 'TypeError: Metaclasses with custom tp_new are not supported.'
# =====================================================================
sys.modules["google._upb._message"] = None

import google.generativeai as genai
from config import Config

# Configure the Gemini Generative AI SDK
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
else:
    # Print warning in development if API key is not supplied
    print("Warning: GEMINI_API_KEY is not set in environment configurations.")

def analyze_eligibility(user_profile, scheme_details):
    """
    Calls the Google Gemini AI model to evaluate eligibility between a citizen's profile
    and a specific government scheme's criteria.
    
    Args:
        user_profile (dict): User demographic profile.
        scheme_details (dict): Government scheme metadata.
        
    Returns:
        dict: Evaluation dictionary containing:
            - eligible (bool)
            - match_percentage (float)
            - ai_explanation (str)
            - missing_requirements (list)
    """
    # Safeguard if API key is not configured: return a mock validation
    if not Config.GEMINI_API_KEY:
        return _generate_fallback_result(user_profile, scheme_details, "No Gemini API key configured.")

    # Formulate a detailed profile description
    profile_summary = f"""
    User Demographic Details:
    - Age: {user_profile.get('age', 'N/A')}
    - Gender: {user_profile.get('gender', 'N/A')}
    - State: {user_profile.get('state', 'N/A')}
    - District: {user_profile.get('district', 'N/A')}
    - Education level: {user_profile.get('education', 'N/A')}
    - Occupation: {user_profile.get('occupation', 'N/A')}
    - Annual Family Income (INR): {user_profile.get('annual_family_income', 'N/A')}
    - Category (e.g. General, OBC, SC, ST, EWS): {user_profile.get('category', 'N/A')}
    - Persons with Disabilities (PwD) Status: {'Disabled' if user_profile.get('is_disabled') == 1 else 'Not Disabled'}
    """

    # Formulate the scheme criteria description
    scheme_summary = f"""
    Government Scheme Details:
    - Title: {scheme_details.get('title', 'N/A')}
    - Description: {scheme_details.get('description', 'N/A')}
    - Category: {scheme_details.get('category', 'N/A')}
    - Eligibility Criteria Description: {scheme_details.get('eligibility_criteria', 'N/A')}
    - Benefits Offered: {scheme_details.get('benefits', 'N/A')}
    - Department: {scheme_details.get('department', 'N/A')}
    """

    # Build the prompt instructing structured JSON output
    prompt = f"""
    You are an expert Government Opportunity Assistant called Citizen Copilot.
    Your task is to analyze the following User Demographic Details against the Government Scheme Details and determine if they qualify.

    {profile_summary}

    {scheme_summary}

    Evaluate the criteria strictly but empathetically. Provide the analysis in JSON format.
    The output MUST be a valid JSON object matching this schema:
    {{
        "eligible": boolean (true if user satisfies eligibility, false otherwise),
        "match_percentage": float/int (score from 0 to 100 based on how well user matches criteria),
        "ai_explanation": "A clear, personalized explanation addressing the user by their details, explaining why they qualify or do not qualify, and outlining any specific terms. Keep it under 4 sentences.",
        "missing_requirements": ["list", "of", "missing", "criteria", "attributes", "that", "prevent", "eligibility", "such as income limits, category, age bounds, or occupation. Leave empty if fully qualified"]
    }}

    Return ONLY the JSON block. Do not include markdown wraps like ```json ... ```. Just raw JSON text.
    """

    try:
        # Use gemini-1.5-flash for speed and cost efficiency
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        raw_text = response.text.strip()
        
        # Clean potential markdown block formatting from model response
        if raw_text.startswith("```"):
            # Remove start block (e.g. ```json or ```)
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        # Parse output JSON
        result = json.loads(raw_text)
        
        # Validate schema keys
        if "eligible" not in result or "match_percentage" not in result:
            raise KeyError("Required keys missing from LLM JSON response.")
            
        # Ensure match_percentage is numeric
        result["match_percentage"] = float(result.get("match_percentage", 0.0))
        result["eligible"] = bool(result.get("eligible", False))
        result["missing_requirements"] = list(result.get("missing_requirements", []))
        
        return result

    except Exception as e:
        # Log error in console and invoke safe local fallback parsing
        print(f"Gemini API invocation error: {str(e)}")
        return _generate_fallback_result(
            user_profile,
            scheme_details,
            f"Failed to fetch analysis from Gemini. Fallback rules executed. Error: {str(e)}"
        )

def _generate_fallback_result(user_profile, scheme_details, error_context=""):
    """
    Generates a fallback evaluation based on clean local heuristics if LLM fails or API key is absent.
    """
    eligible = True
    missing_requirements = []
    
    # 1. Income Heuristic: SC Scholarship limits parents income to 2.5L, Housing (Urban EWS) limit is 3L
    income = user_profile.get("annual_family_income", 0)
    scheme_title = scheme_details.get("title", "")
    
    if "Scholarship" in scheme_title and income > 250000:
        eligible = False
        missing_requirements.append("Annual family income must not exceed ₹2,50,000 for SC Scholarship.")
    elif "Awas Yojana" in scheme_title and income > 300000:
        eligible = False
        missing_requirements.append("Annual family income must not exceed ₹3,00,000 for PMAY-Urban (EWS).")

    # 2. Gender/SHG Heuristic for Lakhpati Didi
    if "Lakhpati Didi" in scheme_title:
        if user_profile.get("gender") != "Female":
            eligible = False
            missing_requirements.append("Must be a female resident to qualify for Lakhpati Didi.")

    # 3. Category match SC Scholarship
    if "SC Students" in scheme_title and user_profile.get("category") != "SC":
        eligible = False
        missing_requirements.append("Must belong to the Scheduled Caste (SC) category.")

    # Calculate mock score
    match_percentage = 100.0 if eligible else max(20.0, 100.0 - (len(missing_requirements) * 30.0))

    if eligible:
        explanation = f"You appear to meet the basic conditions for {scheme_title}. ({error_context})"
    else:
        explanation = f"You do not meet all criteria for {scheme_title}. Details: {', '.join(missing_requirements)} ({error_context})"

    return {
        "eligible": eligible,
        "match_percentage": match_percentage,
        "ai_explanation": explanation,
        "missing_requirements": missing_requirements
    }
