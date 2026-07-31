class Document:
    """
    Represents a Citizen Document upload entity in the platform.
    This class is a pure domain entity and does not perform database queries directly.
    """
    def __init__(self, document_id=None, user_id=None, document_type=None,
                 original_filename=None, stored_file_path=None,
                 upload_timestamp=None, verification_status="Pending"):
        self.document_id = document_id
        self.user_id = user_id
        self.document_type = document_type
        self.original_filename = original_filename
        self.stored_file_path = stored_file_path
        self.upload_timestamp = upload_timestamp
        self.verification_status = verification_status

    @classmethod
    def from_dict(cls, data):
        """
        Factory method to instantiate a Document from a dictionary (e.g. database query result).
        """
        if not data:
            return None
        return cls(
            document_id=data.get("document_id"),
            user_id=data.get("user_id"),
            document_type=data.get("document_type"),
            original_filename=data.get("original_filename"),
            stored_file_path=data.get("stored_file_path"),
            upload_timestamp=data.get("upload_timestamp"),
            verification_status=data.get("verification_status", "Pending")
        )

    def to_dict(self):
        """
        Serializes the document instance into a dictionary.
        """
        return {
            "document_id": self.document_id,
            "user_id": self.user_id,
            "document_type": self.document_type,
            "original_filename": self.original_filename,
            "stored_file_path": self.stored_file_path,
            "upload_timestamp": self.upload_timestamp,
            "verification_status": self.verification_status
        }
