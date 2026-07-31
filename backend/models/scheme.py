import json

class Scheme:
    """
    Represents a Government Opportunity/Scheme entity in the platform.
    This class is a pure domain entity and does not perform database queries directly.
    """
    def __init__(self, scheme_id=None, title=None, description=None, category=None,
                 eligibility_criteria=None, benefits=None, deadline=None,
                 required_documents=None, application_url=None, department=None,
                 created_at=None):
        self.scheme_id = scheme_id
        self.title = title
        self.description = description
        self.category = category
        self.eligibility_criteria = eligibility_criteria
        self.benefits = benefits
        self.deadline = deadline
        # Ensure required_documents is stored as a list internally
        self.required_documents = required_documents if required_documents is not None else []
        self.application_url = application_url
        self.department = department
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """
        Factory method to instantiate a Scheme from a dictionary (e.g. database query result).
        """
        if not data:
            return None

        # Parse required_documents JSON string into a python list
        raw_docs = data.get("required_documents")
        parsed_docs = []
        if raw_docs:
            if isinstance(raw_docs, str):
                try:
                    parsed_docs = json.loads(raw_docs)
                except Exception:
                    parsed_docs = []
            elif isinstance(raw_docs, list):
                parsed_docs = raw_docs

        return cls(
            scheme_id=data.get("scheme_id"),
            title=data.get("title"),
            description=data.get("description"),
            category=data.get("category"),
            eligibility_criteria=data.get("eligibility_criteria"),
            benefits=data.get("benefits"),
            deadline=data.get("deadline"),
            required_documents=parsed_docs,
            application_url=data.get("application_url"),
            department=data.get("department"),
            created_at=data.get("created_at")
        )

    def to_dict(self):
        """
        Serializes the scheme instance into a dictionary.
        """
        return {
            "scheme_id": self.scheme_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "eligibility_criteria": self.eligibility_criteria,
            "benefits": self.benefits,
            "deadline": self.deadline,
            "required_documents": self.required_documents,
            "application_url": self.application_url,
            "department": self.department,
            "created_at": self.created_at
        }
