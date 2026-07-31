from werkzeug.security import check_password_hash

class User:
    """
    Represents a Citizen User entity in the platform.
    This class is a pure domain entity and does not perform database queries directly.
    """
    def __init__(self, user_id=None, full_name=None, email=None, password_hash=None,
                 phone_number=None, age=None, gender=None, state=None, district=None,
                 education=None, occupation=None, annual_family_income=None,
                 category=None, is_disabled=0, created_at=None, updated_at=None):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.phone_number = phone_number
        self.age = age
        self.gender = gender
        self.state = state
        self.district = district
        self.education = education
        self.occupation = occupation
        self.annual_family_income = annual_family_income
        self.category = category
        self.is_disabled = is_disabled
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data):
        """
        Factory method to instantiate a User from a dictionary (e.g. database query result).
        """
        if not data:
            return None
        return cls(
            user_id=data.get("user_id"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            phone_number=data.get("phone_number"),
            age=data.get("age"),
            gender=data.get("gender"),
            state=data.get("state"),
            district=data.get("district"),
            education=data.get("education"),
            occupation=data.get("occupation"),
            annual_family_income=data.get("annual_family_income"),
            category=data.get("category"),
            is_disabled=data.get("is_disabled", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def to_dict(self, exclude_password=True):
        """
        Serializes the user instance into a dictionary.
        """
        user_dict = {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "age": self.age,
            "gender": self.gender,
            "state": self.state,
            "district": self.district,
            "education": self.education,
            "occupation": self.occupation,
            "annual_family_income": self.annual_family_income,
            "category": self.category,
            "is_disabled": self.is_disabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if not exclude_password:
            user_dict["password_hash"] = self.password_hash
        return user_dict

    def check_password(self, plain_password):
        """
        Verifies the user's password using scrypt hash verification.
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, plain_password)
