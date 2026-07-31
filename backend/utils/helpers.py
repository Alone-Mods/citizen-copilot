import json
import re
from datetime import datetime

def format_currency(amount):
    """
    Formats a numeric amount into Indian Rupee currency notation.
    Example: 250000 -> "₹2,50,000"
    """
    if amount is None:
        return "₹0"
    try:
        val = int(amount)
        # Handle zero and negative
        if val == 0:
            return "₹0"
        sign = "-" if val < 0 else ""
        val = abs(val)
        
        s = str(val)
        if len(s) <= 3:
            formatted = s
        else:
            # Indian numbering format: last 3 digits, then groups of 2
            last3 = s[-3:]
            other = s[:-3]
            formatted = ""
            while len(other) > 2:
                formatted = "," + other[-2:] + formatted
                other = other[:-2]
            formatted = other + formatted + "," + last3
            
        return f"{sign}₹{formatted}"
    except (ValueError, TypeError):
        return f"₹{amount}"

def format_date(date_str, output_format="%d %b %Y"):
    """
    Converts YYYY-MM-DD date strings into human-readable date formats.
    Example: "2026-08-31" -> "31 Aug 2026"
    """
    if not date_str or not isinstance(date_str, str):
        return ""
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime(output_format)
    except ValueError:
        return date_str

def sanitize_input(text):
    """
    Strips leading/trailing whitespace and cleans hazardous script/HTML tags from user text inputs.
    """
    if not text or not isinstance(text, str):
        return text
    cleaned = text.strip()
    # Remove <script>...</script> blocks and raw HTML tags
    cleaned = re.sub(r"<script.*?>.*?</script>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    return cleaned

def parse_json_safely(raw_str, default=None):
    """
    Attempts to parse a JSON string safely, returning a fallback default value if parsing fails.
    """
    if default is None:
        default = {}
    if not raw_str:
        return default
    if isinstance(raw_str, (dict, list)):
        return raw_str
    try:
        return json.loads(raw_str)
    except (json.JSONDecodeError, TypeError):
        return default
