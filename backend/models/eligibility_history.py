import json

class EligibilityHistory:
    """
    Represents an AI Eligibility Checking History record.
    This class is a pure domain entity and does not perform database queries directly.
    """
    def __init__(self, history_id=None, user_id=None, scheme_id=None,
                 eligibility_result=None, match_percentage=0.0,
                 ai_explanation=None, missing_requirements=None, checked_at=None,
                 scheme_title=None, scheme_category=None):
        self.history_id = history_id
        self.user_id = user_id
        self.scheme_id = scheme_id
        self.eligibility_result = eligibility_result
        self.match_percentage = match_percentage
        self.ai_explanation = ai_explanation
        # Ensure missing_requirements is stored as a list internally
        self.missing_requirements = missing_requirements if missing_requirements is not None else []
        self.checked_at = checked_at
        
        # Joined fields for convenience in UI listings
        self.scheme_title = scheme_title
        self.scheme_category = scheme_category

    @classmethod
    def from_dict(cls, data):
        """
        Factory method to instantiate EligibilityHistory from a dictionary.
        """
        if not data:
            return None

        # Parse missing_requirements JSON string into a python list
        raw_reqs = data.get("missing_requirements")
        parsed_reqs = []
        if raw_reqs:
            if isinstance(raw_reqs, str):
                try:
                    parsed_reqs = json.loads(raw_reqs)
                except Exception:
                    parsed_reqs = []
            elif isinstance(raw_reqs, list):
                parsed_reqs = raw_reqs

        return cls(
            history_id=data.get("history_id"),
            user_id=data.get("user_id"),
            scheme_id=data.get("scheme_id"),
            eligibility_result=data.get("eligibility_result"),
            match_percentage=data.get("match_percentage", 0.0),
            ai_explanation=data.get("ai_explanation"),
            missing_requirements=parsed_reqs,
            checked_at=data.get("checked_at"),
            scheme_title=data.get("scheme_title"),
            scheme_category=data.get("scheme_category")
        )

    def to_dict(self):
        """
        Serializes the eligibility history instance into a dictionary.
        """
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "scheme_id": self.scheme_id,
            "eligibility_result": self.eligibility_result,
            "match_percentage": self.match_percentage,
            "ai_explanation": self.ai_explanation,
            "missing_requirements": self.missing_requirements,
            "checked_at": self.checked_at,
            "scheme_title": self.scheme_title,
            "scheme_category": self.scheme_category
        }
