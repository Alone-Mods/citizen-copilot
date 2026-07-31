import re

def validate_email(email):
    """
    Validates if an email address string is properly formatted.
    """
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.strip()) is not None

def validate_phone(phone_number):
    """
    Validates an Indian 10-digit phone number.
    """
    if not phone_number:
        return True  # Optional field
    phone_str = str(phone_number).strip()
    pattern = r"^[6-9]\d{9}$"
    return re.match(pattern, phone_str) is not None

def validate_income(annual_family_income):
    """
    Validates that annual family income is a non-negative number.
    """
    if annual_family_income is None:
        return True
    try:
        val = float(annual_family_income)
        return val >= 0
    except (ValueError, TypeError):
        return False

def validate_age(age):
    """
    Validates that age is an integer between 0 and 120.
    """
    if age is None:
        return True
    try:
        val = int(age)
        return 0 <= val <= 120
    except (ValueError, TypeError):
        return False

def validate_category(category):
    """
    Validates that category belongs to recognized Indian administrative social groups.
    """
    if not category:
        return True
    valid_categories = {"General", "OBC", "SC", "ST", "EWS"}
    return str(category).strip() in valid_categories

def validate_gender(gender):
    """
    Validates gender value against supported gender options.
    """
    if not gender:
        return True
    valid_genders = {"Male", "Female", "Non-Binary", "Other", "Prefer Not to Say"}
    return str(gender).strip() in valid_genders
