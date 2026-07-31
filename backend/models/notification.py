class Notification:
    """
    Represents a User Notification entity in the platform.
    This class is a pure domain entity and does not perform database queries directly.
    """
    def __init__(self, notification_id=None, user_id=None, title=None, message=None,
                 notification_type=None, is_read=0, created_at=None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.is_read = is_read
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """
        Factory method to instantiate a Notification from a dictionary (e.g. database query result).
        """
        if not data:
            return None
        return cls(
            notification_id=data.get("notification_id"),
            user_id=data.get("user_id"),
            title=data.get("title"),
            message=data.get("message"),
            notification_type=data.get("notification_type"),
            is_read=data.get("is_read", 0),
            created_at=data.get("created_at")
        )

    def to_dict(self):
        """
        Serializes the notification instance into a dictionary.
        """
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "is_read": self.is_read,
            "created_at": self.created_at
        }
